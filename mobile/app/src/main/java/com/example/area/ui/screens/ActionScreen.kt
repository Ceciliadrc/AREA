package com.example.area.ui.screens

import android.text.Layout
import android.util.Log
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.area.data.repository.ServiceRepository
import com.example.area.ui.theme.*
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Preview(showBackground = true)
@Composable
fun ActionScreen (
    modifier: Modifier = Modifier,
) {
    var services by remember { mutableStateOf<List<com.example.area.data.models.Service>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null)}

    val context = LocalContext.current
    val scope = rememberCoroutineScope()

    LaunchedEffect(Unit) {
        scope.launch {
            val serviceRepository = ServiceRepository(context)
            val result = serviceRepository.getAllServices()

            isLoading = false

            if (result.isSuccess) {
                services = result.getOrThrow().services
                errorMessage = null
                Log.d("ActionScreen", "Loaded ${services.size} services")
            } else {
                errorMessage = result.exceptionOrNull()?.message
                Log.e("ActionScreen", "Failed to load services AAAAAAAAH: $errorMessage")
            }
        }
    }

    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = {
                    Text(
                        "Choose the trigger",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.Black
                    )
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.Transparent,
                    titleContentColor = Color.White
                ),

            )
        },
        containerColor = Color.Transparent
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(color = Blush)
                .padding(paddingValues)
        ) {
            when {
                isLoading -> {
                    Box(
                        modifier = Modifier.fillMaxSize(),
                        contentAlignment = Alignment.Center
                    ) {
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            CircularProgressIndicator(
                                color = Peony,
                                modifier = Modifier.size(60.dp)
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            Text(
                                text = "Loading services...",
                                color = Color.Black,
                                fontSize = 16.sp
                            )
                        }
                    }
                }
                errorMessage != null -> {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(24.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Box(
                            modifier = Modifier
                                .size(120.dp)
                                .clip(CircleShape)
                                .background(
                                    brush = Brush.linearGradient(
                                        colors = listOf(Peony, Mauve)
                                    )
                                ),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                Icons.Default.Warning,
                                contentDescription = "Error",
                                tint = Color.White,
                                modifier = Modifier.size(60.dp)
                            )
                        }

                        Spacer(modifier = Modifier.height(32.dp))

                        Text(
                            text = "Failed to load services",
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.White
                        )

                        Spacer(modifier = Modifier.height(16.dp))

                        Text(
                            text = errorMessage ?: "Unknown error",
                            fontSize = 16.sp,
                            color = Color.White.copy(alpha = 0.8f),
                            textAlign = TextAlign.Center
                        )

                        Spacer(modifier = Modifier.height(32.dp))

                        Button(
                            onClick = {
                                isLoading = true
                                errorMessage = null
                                scope.launch {
                                    val serviceRepository = ServiceRepository(context)
                                    val result = serviceRepository.getAllServices()

                                    isLoading = false

                                    if (result.isSuccess) {
                                        services = result.getOrThrow().services
                                        errorMessage = null
                                    } else {
                                        errorMessage = result.exceptionOrNull()?.message
                                    }
                                }
                            },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Peony
                            )
                        ) {
                            Text("Retry")
                        }
                    }
                }
                services.isEmpty() -> {
                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(24.dp),
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Center
                    ) {
                        Box(
                            modifier = Modifier
                                .size(120.dp)
                                .clip(CircleShape)
                                .background(
                                    brush = Brush.linearGradient(
                                        colors = listOf(Peony, Mauve)
                                    )
                                ),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                Icons.Default.Warning,
                                contentDescription = "No Services",
                                tint = Color.White,
                                modifier = Modifier.size(60.dp)
                            )
                        }

                        Spacer(modifier = Modifier.height(32.dp))

                        Text(
                            text = "No services available",
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color.White
                        )

                        Spacer(modifier = Modifier.height(16.dp))

                        Text(
                            text = "The server doesn't have any services configured yet",
                            fontSize = 16.sp,
                            color = Color.White.copy(alpha = 0.8f),
                            textAlign = TextAlign.Center
                        )
                    }
                }
                else -> {
                    LazyColumn(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(horizontal = 24.dp, vertical = 16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        item {
                            Card(
                                modifier = Modifier.fillMaxWidth(),
                                colors = CardDefaults.cardColors(
                                    containerColor = Color.White.copy(alpha = 0.9f)
                                ),
                                elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
                                shape = RoundedCornerShape(16.dp)
                            ) {
                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(20.dp)
                                ) {
                                    Text(
                                        text = "Available Triggers",
                                        fontSize = 18.sp,
                                        fontWeight = FontWeight.Bold,
                                        color = Graphite
                                    )

                                    Spacer(modifier = Modifier.height(8.dp))

                                    Text(
                                        text = "Select a service to create an Action. Connect more services in your Profile to unlock additional triggers.",
                                        fontSize = 14.sp,
                                        color = Graphite.copy(alpha = 0.7f),
                                        lineHeight = 20.sp
                                    )

                                    Spacer(modifier = Modifier.height(12.dp))

                                    Text(
                                        text = "Services available: ${services.size}",
                                        fontSize = 14.sp,
                                        color = Peony,
                                        fontWeight = FontWeight.Medium
                                    )
                                }
                            }
                        }

                        items(services) { service ->
                            ServiceCard(
                                service = service,
                                onClick = {
                                    when (service.name.lowercase()) {
                                        "timer", "clock" -> {
                                            // TODO: navController.navigate("clockTrigger")
                                        }
                                    }
                                }
                            )
                        }

                        // Add extra spacing at bottom for nav bar
                        item {
                            Spacer(modifier = Modifier.height(80.dp))
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun ServiceCard(
    service: com.example.area.data.models.Service,
    onClick: () -> Unit,
) {
    val icon = when (service.name.lowercase()) {
        "timer", "clock" -> Icons.Default.WatchLater
        "spotify", "music" -> Icons.Default.MusicNote
        "twitch", "stream" -> Icons.Default.OndemandVideo
        "instagram", "facebook", "social" -> Icons.Default.CameraAlt
        "openai", "ai", "chatgpt" -> Icons.Default.Computer
        "notion", "notes" -> Icons.Default.NoteAlt
        "gmail", "email", "outlook" -> Icons.Default.Email
        else -> Icons.Default.Apps
    }
    val description = when (service.name.lowercase()) {
        "timer", "clock" -> "Time-based triggers"
        "spotify" -> "Music and playlist triggers"
        "twitch" -> "Stream and chat triggers"
        "instagram" -> "Post and message triggers"
        "openai" -> "AI-powered triggers"
        "notion" -> "Document and database triggers"
        "gmail" -> "Email-based triggers"
        else -> "${service.displayName} triggers"
    }

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        colors = CardDefaults.cardColors(
            containerColor = Color.Transparent
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
        shape = RoundedCornerShape(16.dp)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(
                    brush = Brush.linearGradient(
                        colors = listOf(Color.White, Blush)
                    )
                )
                .border(
                    width = 2.dp,
                    color = Peony.copy(alpha = 0.7f),
                    shape = RoundedCornerShape(16.dp)
                )
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(20.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box(
                    modifier = Modifier
                        .size(56.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Peony),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = icon,
                        contentDescription = service.name,
                        tint = Color.White,
                        modifier = Modifier.size(28.dp)
                    )
                }

                Spacer(modifier = Modifier.width(16.dp))

                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = service.name,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = Graphite
                    )

                    Spacer(modifier = Modifier.height(4.dp))

                    Text(
                        text = description,
                        fontSize = 14.sp,
                        color = Graphite.copy(alpha = 0.7f),
                        maxLines = 2
                    )
                }

                Icon(
                    Icons.Default.KeyboardArrowRight,
                    contentDescription = "Select",
                    tint = Peony,
                    modifier = Modifier.size(20.dp)
                )
            }
        }
    }
}

// CHANGE ALLAT WHEN YOU FINALLY DID THE API CONNECTION SETUP LMAO
data class Service(
    val id: String,
    val name: String,
    val icon: androidx.compose.ui.graphics.vector.ImageVector,
    val isConnected: Boolean,
    val description: String
)