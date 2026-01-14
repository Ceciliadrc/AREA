package com.example.area.ui.components

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Email
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.area.ui.theme.*

@Composable
fun LabeledTextField(
    label: String,
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    placeholder: String = "",
    isPassword: Boolean = false,
    keyboardType: KeyboardType = KeyboardType.Text,
    imeAction: ImeAction = ImeAction.Next,
    leadingIcon: @Composable (() -> Unit)? = null,
    singleLine: Boolean = true
) {
    Column(
        modifier = modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.Start
    ) {
        Text(
            label,
            fontSize = 18.sp,
            color = Mauve,
            modifier = Modifier.padding(start = 4.dp)
        )

        Spacer(modifier = Modifier.height(4.dp))

        OutlinedTextField(
            value = value,
            onValueChange = onValueChange,
            modifier = Modifier.fillMaxWidth(),
            placeholder = { Text(placeholder) },
            leadingIcon = leadingIcon,
            singleLine = singleLine,
            keyboardOptions = KeyboardOptions(
                keyboardType = keyboardType,
                imeAction = imeAction
            ),
            visualTransformation = if (isPassword) PasswordVisualTransformation() else VisualTransformation.None,
            /*colors = OutlinedTextFieldDefaults.colors(
                focusedBorderColor = Mauve,
                unfocusedBorderColor = Mauve.copy(alpha = 0.5f),
                focusedLeadingIconColor = Mauve,
                unfocusedLeadingIconColor = Mauve.copy(alpha = 0.5f),
                cursorColor = Mauve,
                textColor = Color.Black
            )*/
        )
    }
}

@Composable
fun EmailField(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    LabeledTextField(
        label = "Email",
        value = value,
        onValueChange = onValueChange,
        modifier = modifier,
        placeholder = "your.email@area.com",
        keyboardType = KeyboardType.Email,
        leadingIcon = {
            Icon(Icons.Default.Email, contentDescription = "Email", tint = Mauve)
        }
    )
}

@Composable
fun PasswordField(
    label: String = "Password",
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier,
    imeAction: ImeAction = ImeAction.Next
) {
    LabeledTextField(
        label = label,
        value = value,
        onValueChange = onValueChange,
        modifier = modifier,
        placeholder = "********",
        isPassword = true,
        imeAction = imeAction,
        leadingIcon = {
            Icon(Icons.Default.Lock, contentDescription = "Password", tint = Mauve)
        }
    )
}

@Composable
fun UsernameField(
    value: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    LabeledTextField(
        label = "Username",
        value = value,
        onValueChange = onValueChange,
        modifier = modifier,
        placeholder = "choose a username",
        leadingIcon = {
            Icon(Icons.Default.Person, contentDescription = "Username", tint = Mauve)
        }
    )
}