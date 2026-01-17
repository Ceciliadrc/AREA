package com.example.area.ui.screens

import android.app.Activity
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.area.auth.googleAuthFlow
import com.example.area.ui.theme.*
import com.example.area.ui.components.*
import com.example.area.R
import kotlinx.coroutines.launch
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import com.example.area.data.repository.AuthRepository
import com.example.area.data.repository.RepositoryManager

@OptIn(ExperimentalMaterial3Api::class)
@Preview(showBackground = true)
@Composable
fun LoginScreen (
    modifier: Modifier = Modifier,
    onLoginSuccess: () -> Unit = {},
    onNavigateToRegister: () -> Unit = {},
    onNavigateToForgotPassword: () -> Unit = {}
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var rememberMe by remember { mutableStateOf(false) }
    var isLoading by remember { mutableStateOf(false) }
    var showServerDialog by remember { mutableStateOf(false) }

    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val activity = context as? Activity
    val authRepository = remember { RepositoryManager.getAuthRepository(context) }

    ServerConfigDialog(
        isVisible = showServerDialog,
        onDismiss = { showServerDialog = false },
        onSave = {
            showServerDialog = false
            Toast.makeText(context, "Server settings saved", Toast.LENGTH_SHORT).show()
        }
    )

    GradientBackground {
        AuthContainer(
            title = "Welcome",
            subtitle = "Login"
        ) {
            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(24.dp)
            ) {
                EmailField(
                    value = email,
                    onValueChange = { email = it }
                )

                PasswordField(
                    value = password,
                    onValueChange = { password = it }
                )

                RememberMeAndForgotPasswordRow(
                    rememberMe = rememberMe,
                    onRememberMeChange = { rememberMe = it },
                    onForgotPasswordClick = onNavigateToForgotPassword
                )

                GradientButton(
                    text = "Login",
                    onClick = {
                        if (email.isNotEmpty() && password.isNotEmpty()) {
                            isLoading = true
                            scope.launch {
                                val result = authRepository.login(email, password)
                                isLoading = false

                                if (result.isSuccess) {
                                    val userResponse = result.getOrNull()
                                    if (userResponse?.error != null) {
                                        Toast.makeText(context, userResponse.error, Toast.LENGTH_SHORT).show()
                                    } else {
                                        val message = userResponse?.message ?: "Login successful!"
                                        Toast.makeText(context, message, Toast.LENGTH_SHORT).show()
                                        onLoginSuccess()
                                    }
                                } else {
                                    val errorMessage = result.exceptionOrNull()?.message ?: "Unknown error"
                                    Toast.makeText(context, "Login failed: $errorMessage", Toast.LENGTH_SHORT).show()
                                }
                            }
                        } else {
                            Toast.makeText(context, "Please fill in all fields", Toast.LENGTH_SHORT).show()
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    isLoading = isLoading
                )

                OrDivider()
                Text("Login with", fontSize = 18.sp, color = Mauve, modifier = Modifier.align(Alignment.CenterHorizontally))
                OAuthButtonsRow(
                    onGoogleClick = {
                        scope.launch {
                            googleAuthFlow(
                                context = context,
                                activity = activity,
                                webClientId = context.getString(R.string.google_web_client_id),
                                authRepository = authRepository,
                                successToast = "Logged in w Google!",
                                onSuccess = onLoginSuccess
                            )
                        }
                    }
                )
                Spacer(modifier = Modifier.height(18.dp))
                OrDivider()
                RegisterLink(
                    onNavigateToRegister = onNavigateToRegister
                )

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.Center
                ) {
                    ServerConfigLink(
                        onClick = { showServerDialog = true }
                    )
                }
            }
        }
    }
}

@Composable
fun RememberMeAndForgotPasswordRow(
    rememberMe: Boolean,
    onRememberMeChange: (Boolean) -> Unit,
    onForgotPasswordClick: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Checkbox(
                checked = rememberMe,
                onCheckedChange = onRememberMeChange,
                colors = CheckboxDefaults.colors(
                    checkedColor = Mauve,
                    uncheckedColor = Mauve.copy(alpha = 0.5f),
                    checkmarkColor = Color.White
                )
            )
            Text("Remember me", fontSize = 14.sp, color = Mauve)
        }
        Text(
            text = "Forgot password?",
            fontSize = 14.sp,
            color = Mauve,
            modifier = Modifier.clickable { onForgotPasswordClick() }
        )
    }
}

@Composable
fun OAuthButtonsRow(
    onGoogleClick: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceEvenly
    ) {
        OAuthButton(
            text = "Google",
            onClick = onGoogleClick,
            color = Mauve
        )

        // like...add others if we got any time
    }
}

@Composable
fun RegisterLink(
    onNavigateToRegister: () -> Unit
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Don't have an account yet? ",
            fontSize = 18.sp,
            color = Mauve
        )
        Text(
            text = "Register now",
            fontSize = 18.sp,
            color = Mauve,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.clickable { onNavigateToRegister() }
        )
    }
}