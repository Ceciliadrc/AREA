package com.example.area.ui.screens

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.area.ui.theme.*
import com.example.area.ui.components.*
import androidx.compose.runtime.rememberCoroutineScope
import com.example.area.data.repository.AuthRepository
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.ui.focus.focusModifier
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Preview(showBackground = true)
@Composable
fun RegisterScreen(
    modifier: Modifier = Modifier,
    onRegisterSuccess: () -> Unit = {},
    onNavigateToLogin: () -> Unit = {}
) {
    var username by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var isLoading by remember { mutableStateOf(false) }

    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val authRepository = remember { AuthRepository(context) }

    GradientBackground {
        AuthContainer(
            title = "Welcome",
            subtitle = "Create account"
        ) {
            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(20.dp)
            ) {
                UsernameField(
                    value = username,
                    onValueChange = { username = it }
                )

                PasswordField(
                    label = "Password",
                    value = password,
                    onValueChange = { password = it }
                )

                PasswordField(
                    label = "Confirm Password",
                    value = confirmPassword,
                    onValueChange = { confirmPassword = it },
                    imeAction = ImeAction.Done
                )

                EmailField(
                    value = email,
                    onValueChange = { email = it }
                )

                GradientButton(
                    text = "Register",
                    onClick = {
                        if (username.isEmpty() || email.isEmpty() || password.isEmpty() || confirmPassword.isEmpty()) {
                            Toast.makeText(context, "Please fill in all fields", Toast.LENGTH_SHORT)
                                .show()
                        } else if (password != confirmPassword) {
                            Toast.makeText(context, "Passwords don't match", Toast.LENGTH_SHORT)
                                .show()
                        } else {
                            Toast.makeText(context, "Creating account...", Toast.LENGTH_SHORT)
                                .show()
                            isLoading = true
                            scope.launch {
                                val result = authRepository.register(username, email, password)
                                isLoading = false
                                if (result.isSuccess) {
                                    val userResponse = result.getOrNull()
                                    val message = userResponse?.message ?: "Registration successful!"
                                    Toast.makeText(context, message, Toast.LENGTH_SHORT).show()
                                    onRegisterSuccess()
                                } else {
                                    val errorMessage = result.exceptionOrNull()?.message ?: "Unknown error"
                                    Toast.makeText(context, "Registration failed: $errorMessage", Toast.LENGTH_SHORT).show()
                                }
                            }
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    isLoading = isLoading
                )

                OrDivider()
                Text("Sign up with", fontSize = 16.sp, color = Mauve, fontWeight = FontWeight.Medium, modifier = Modifier.align(Alignment.CenterHorizontally))
                OAuthButtonsRow()
                LoginLink(
                    onNavigateToLogin = onNavigateToLogin
                )
            }
        }
    }
}

@Composable
fun LoginLink(
    onNavigateToLogin: () -> Unit
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Already have an account? ",
            fontSize = 16.sp,
            color = Mauve
        )
        Text(
            text = "Login",
            fontSize = 16.sp,
            color = Mauve,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.clickable { onNavigateToLogin() }
        )
    }
}