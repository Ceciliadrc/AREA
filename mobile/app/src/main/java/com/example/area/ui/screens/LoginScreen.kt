package com.example.area.ui.screens

import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.Divider
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TextFieldColors
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
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
import com.example.area.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Preview(showBackground = true)
@Composable
fun LoginScreen (
    modifier: Modifier = Modifier,
    onLoginSuccess: () -> Unit = {},
    onNavigateToRegister: () -> Unit = {}
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var rememberMe by remember { mutableStateOf(false) }
    val context = LocalContext.current

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(
                        Blush,
                        Peony
                    )
                )
            ),
        contentAlignment = Alignment.Center
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(32.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text("Welcome", fontSize = 40.sp, fontWeight = FontWeight.Bold)
            Spacer(modifier = Modifier.height(8.dp))

            Text("Login", fontSize = 20.sp, color = Mauve)
            Spacer(modifier = Modifier.height(72.dp))

            Column(modifier = Modifier.fillMaxWidth(), horizontalAlignment = Alignment.Start) {
                Text(
                    "Email",
                    fontSize = 18.sp,
                    color = Mauve,
                    modifier = Modifier.padding(start = 4.dp)
                )

                Spacer(modifier = Modifier.height(4.dp))

                OutlinedTextField(
                    value = email,
                    onValueChange = {email = it },
                    modifier = Modifier.fillMaxWidth(),
                    placeholder = { Text("your.email@area.com") },
                    /*colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = Mauve,
                        unfocusedBorderColor = Mauve.copy(alpha = 0.5f),
                        focusedLabelColor = Mauve,
                        unfocusedLabelColor = Mauve.copy(alpha = 0.5f),
                        cursorColor = Mauve,
                        textColor = Color.White
                    ),*/
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Next),
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            Column(modifier = Modifier.fillMaxWidth(), horizontalAlignment = Alignment.Start) {
                Text(
                    "Password",
                    fontSize = 18.sp,
                    color = Mauve,
                    modifier = Modifier.padding(start = 4.dp)
                )

                Spacer(modifier = Modifier.height(2.dp))

                OutlinedTextField(
                    value = password,
                    onValueChange = { password = it },
                    label = { Text("********") },
                    visualTransformation = PasswordVisualTransformation(),
                    modifier = Modifier.fillMaxWidth()
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Start,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Checkbox(
                    checked = rememberMe,
                    onCheckedChange = { rememberMe = it },
                    colors = CheckboxDefaults.colors(
                        checkedColor = Mauve,
                        uncheckedColor = Mauve.copy(alpha = 0.5f),
                        checkmarkColor = Color.White
                    )
                )

                Text(
                    text = "Remember me",
                    fontSize = 14.sp,
                    color = Mauve
                )

                Spacer(modifier = Modifier.width(72.dp))

                Text(
                    text = "Forgot password?",
                    fontSize = 14.sp,
                    color = Mauve,
                    modifier = Modifier.clickable {
                        // TODO: Navigate to forgot password screen
                    }
                )
            }

            Spacer(modifier = Modifier.height(32.dp))

            Button(
                onClick = {
                    if (email.isNotEmpty() && password.isNotEmpty()) {
                        Toast.makeText(context, "Logging in...", Toast.LENGTH_SHORT).show()
                        // TODO: API CALLLLLLLLLL
                        onLoginSuccess()
                    } else {
                        Toast.makeText(context, "Please fill in all fields", Toast.LENGTH_SHORT).show()
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp)
                    .background(
                        brush = Brush.linearGradient(
                            colors = listOf(
                                Peony,
                                Mauve
                            )
                        ),
                        shape = MaterialTheme.shapes.medium
                    ),
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.Transparent
                ),
                shape = MaterialTheme.shapes.medium
            ) {
                Text(
                    text = "Login →",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Medium
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                HorizontalDivider(
                    modifier = Modifier
                        .weight(1f)
                        .height(3.dp),
                    color = Mauve
                )

                Text(
                    text = "or",
                    fontSize = 18.sp,
                    color = Mauve,
                    modifier = Modifier.padding(horizontal = 16.dp)
                )

                HorizontalDivider(
                    modifier = Modifier
                        .weight(1f)
                        .height(3.dp),
                    color = Mauve
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            // OAuth Buttons (really need to add them or wtv)
            Text(
                text = "login with",
                fontSize = 18.sp,
                color = Mauve
            )

            Spacer(modifier = Modifier.height(16.dp))

            Text(
                text = "[Where my OAuth 2 buttons atttt]",
                fontSize = 12.sp,
                color = Mauve.copy(alpha = 0.7f),
                fontStyle = androidx.compose.ui.text.font.FontStyle.Italic
            )

            Spacer(modifier = Modifier.height(32.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                HorizontalDivider(
                    modifier = Modifier
                        .weight(1f)
                        .height(3.dp),
                    color = Mauve
                )

                Text(
                    text = "or",
                    fontSize = 18.sp,
                    color = Mauve,
                    modifier = Modifier.padding(horizontal = 16.dp)
                )

                HorizontalDivider(
                    modifier = Modifier
                        .weight(1f)
                        .height(3.dp),
                    color = Mauve
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

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
                modifier = Modifier.clickable {
                    onNavigateToRegister()
                }
            )
        }
    }
}

//FUCKING HELL WITH IT OH MY GOSH GODS
/*@OptIn(ExperimentalMaterial3Api::class)
fun customTextFieldColors(): TextFieldColors {
    return OutlinedTextFieldDefaults.colors(
        focusedBorderColor = Mauve,
        unfocusedBorderColor = Mauve.copy(alpha = 0.7f),
        focusedLabelColor = Mauve,
        unfocusedLabelColor = Mauve.copy(alpha = 0.7f),
        cursorColor = Mauve,
        textColor = Color.Black,
        containerColor = Color.White,
        focusedTextColor = Color.Black,
        unfocusedTextColor = Color.Black.copy(alpha = 0.8f),
        placeholderColor = Color.Gray,
        focusedLeadingIconColor = Mauve,
        unfocusedLeadingIconColor = Mauve.copy(alpha = 0.7f),
    )
}*/

@Composable
fun GoogleLoginButton(onClick: () -> Unit) {
    // Implement Google OAuth button
}

@Composable
fun GithubLoginButton(onClick: () -> Unit) {
    // Implement Facebook OAuth button
}

@Composable
fun FacebookLoginButton(onClick: () -> Unit) {
    // Implement Twitter/X OAuth button
}