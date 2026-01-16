package com.example.area.ui.components

import androidx.compose.foundation.border
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Wifi
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.example.area.data.api.ApiClient
import com.example.area.ui.theme.*
import androidx.compose.ui.platform.LocalContext
import androidx.compose.foundation.clickable
import androidx.compose.foundation.shape.RoundedCornerShape
import kotlinx.coroutines.launch

@Composable
fun ServerConfigDialog(
    isVisible: Boolean,
    onDismiss: () -> Unit,
    onSave: () -> Unit
) {
    var serverIp by remember { mutableStateOf("") }
    var port by remember { mutableStateOf("8080") }
    var testResult by remember { mutableStateOf<String?>(null) }
    var isLoading by remember { mutableStateOf(false) }
    val context = LocalContext.current
    val scope = rememberCoroutineScope()

    LaunchedEffect(isVisible) {
        if (isVisible) {
            val currentUrl = ApiClient.getCurrentBaseUrl(context)
            val regex = """http://([^:]+):(\d+)""".toRegex()
            val match = regex.find(currentUrl)
            if (match != null) {
                serverIp = match.groupValues[1]
                port = match.groupValues[2]
            }
        }
    }

    if (isVisible) {
        Dialog(onDismissRequest = onDismiss) {
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                shape = MaterialTheme.shapes.large,
                elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(24.dp)
                        .verticalScroll(rememberScrollState()),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.Wifi,
                            contentDescription = "Server Config",
                            tint = Peony,
                            modifier = Modifier.size(24.dp)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = "Server Configuration",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold,
                            color = Graphite
                        )
                    }
                }

                Text(
                    text = "Configure the IP address and port of your AREA server",
                    fontSize = 14.sp,
                    color = Graphite.copy(alpha = 0.7f),
                    textAlign = TextAlign.Center
                )

                Column(modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = "Server IP Address",
                        fontSize = 14.sp,
                        color = Mauve,
                        fontWeight = FontWeight.Medium,
                        modifier = Modifier.padding(bottom = 4.dp)
                    )
                    OutlinedTextField(
                        value = serverIp,
                        onValueChange = { serverIp = it },
                        modifier = Modifier.fillMaxWidth(),
                        placeholder = { Text("e.g., 192.168.1.100") },
                        singleLine = true,
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Peony,
                            unfocusedBorderColor = Peony.copy(alpha = 0.5f),
                            cursorColor = Peony
                        )
                    )
                }

                Column(modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = "Port",
                        fontSize = 14.sp,
                        color = Mauve,
                        fontWeight = FontWeight.Medium,
                        modifier = Modifier.padding(bottom = 4.dp)
                    )
                    OutlinedTextField(
                        value = port,
                        onValueChange = { port = it },
                        modifier = Modifier.fillMaxWidth(),
                        placeholder = { Text("8080") },
                        singleLine = true,
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedBorderColor = Peony,
                            unfocusedBorderColor = Peony.copy(alpha = 0.5f),
                            cursorColor = Peony
                        )
                    )
                }

                Column(modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = "Common IPs to try:",
                        fontSize = 12.sp,
                        color = Graphite.copy(alpha = 0.7f),
                        modifier = Modifier.padding(bottom = 4.dp)
                    )
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        listOf("192.168.1.100", "10.0.2.2", "10.0.0.100").forEach { ip ->
                            Box(
                                modifier = Modifier
                                    .clickable { serverIp = ip }
                                    .border(
                                        width = 1.dp,
                                        color = if (serverIp == ip) Peony else Mauve.copy(alpha = 0.3f),
                                        shape = RoundedCornerShape(16.dp)
                                    )
                                    .background(
                                        color = if (serverIp == ip) Peony else Mauve.copy(alpha = 0.3f),
                                        shape = RoundedCornerShape(16.dp)
                                    )
                                    .padding(horizontal = 12.dp, vertical = 6.dp)
                            ) {
                                Text(ip, fontSize = 12.sp, color = if (serverIp == ip) Color.White else Graphite)
                            }
                        }
                    }
                }

                Button(
                    onClick = {
                        if (serverIp.isNotEmpty()) {
                            isLoading = true
                            testResult = null
                            scope.launch {
                                val testUrl =
                                    "http://$serverIp:${port.takeIf { it.isNotEmpty() } ?: "8080"}"
                                // Temporarily update API client for test
                                ApiClient.updateBaseUrl(context, testUrl)

                                // Create a test repository
                                val testRepo =
                                    com.example.area.data.repository.AuthRepository(context)
                                val isConnected = testRepo.testConnection()

                                isLoading = false
                                testResult = if (isConnected) {
                                    "Successfully connected to server!"
                                } else {
                                    "Could not connect to server"
                                }
                            }
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Blossom
                    ),
                    enabled = serverIp.isNotEmpty() && !isLoading
                ) {
                    if (isLoading) {
                        CircularProgressIndicator(
                            color = Color.White,
                            modifier = Modifier.size(16.dp)
                        )
                    } else {
                        Text("Test Connection")
                    }
                }

                testResult?.let { result ->
                    Text(
                        text = result,
                        fontSize = 13.sp,
                        color = if (result.startsWith("S")) Color(0xFF2E7D32) else Color.Red,
                        textAlign = TextAlign.Center
                    )

                    Spacer(modifier = Modifier.height(8.dp))

                    // Action Buttons
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        // Cancel Button
                        OutlinedButton(
                            onClick = onDismiss,
                            modifier = Modifier.weight(1f),
                            colors = ButtonDefaults.outlinedButtonColors(
                                contentColor = Graphite
                            )
                        ) {
                            Text("Cancel")
                        }

                        Button(
                            onClick = {
                                if (serverIp.isNotEmpty()) {
                                    val baseUrl =
                                        "http://$serverIp:${port.takeIf { it.isNotEmpty() } ?: "8080"}"
                                    ApiClient.updateBaseUrl(context, baseUrl)
                                    onSave()
                                }
                            },
                            modifier = Modifier.weight(1f),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Peony
                            ),
                            enabled = serverIp.isNotEmpty() && testResult?.startsWith("S") == true
                        ) {
                            Text("Save")
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ServerConfigButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    IconButton(
        onClick = onClick,
        modifier = modifier
    ) {
        Icon(
            Icons.Default.Settings,
            contentDescription = "Configure Server",
            tint = Mauve,
            modifier = Modifier.size(24.dp)
        )
    }
}

@Composable
fun ServerConfigLink(
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Text(
        text = "Change server",
        fontSize = 14.sp,
        color = Mauve.copy(alpha = 0.7f),
        modifier = modifier.clickable { onClick() }
    )
}