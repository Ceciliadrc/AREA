package com.example.area.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.area.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Preview(showBackground = true)
@Composable
fun ActionScreen (
    modifier: Modifier = Modifier,
) {
    val services = remember {
        listOf(
            Service(
                id = "clock",
                name = "Clock",
                icon = Icons.Default.WatchLater,
                isConnected = true,
                description = "Time-based triggers"
            ),
            Service(
                id = "spotify",
                name = "Spotify",
                icon = Icons.Default.MusicNote,
                isConnected = false,
                description = "Music and playlist triggers"
            ),
            Service(
                id = "twitch",
                name = "Twitch",
                icon = Icons.Default.OndemandVideo,
                isConnected = false,
                description = "Stream and chat triggers"
            ),
            Service(
                id = "instagram",
                name = "Instagram",
                icon = Icons.Default.CameraAlt,
                isConnected = false,
                description = "Post and message triggers"
            ),
            Service(
                id = "openai",
                name = "OpenAI",
                icon = Icons.Default.Computer,
                isConnected = false,
                description = "AI-powered triggers"
            ),
            Service(
                id = "notion",
                name = "Notion",
                icon = Icons.Default.NoteAlt,
                isConnected = false,
                description = "Document and database triggers"
            ),
            Service(
                id = "gmail",
                name = "Gmail",
                icon = Icons.Default.Email,
                isConnected = false,
                description = "Email-based triggers"
            )
        )
    }

    val connectedServices = services.filter { it.isConnected }

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
            if (connectedServices.isEmpty()) {
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
                        text = "No connected services",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    Text(
                        text = "Connect services in your Profile to create triggers",
                        fontSize = 16.sp,
                        color = Color.White.copy(alpha = 0.8f),
                        textAlign = androidx.compose.ui.text.style.TextAlign.Center
                    )
                }
            } else {
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
                                    text = "Connected: ${connectedServices.size}/${services.size}",
                                    fontSize = 14.sp,
                                    color = Peony,
                                    fontWeight = FontWeight.Medium
                                )
                            }
                        }
                    }

                    // Connected services
                    items(connectedServices) { service ->
                        ServiceCard(
                            service = service,
                            onClick = {
                                when (service.id) {
                                    "clock" -> {
                                        // Navigate to clock trigger selection
                                        // TODO: navController.navigate("clockTrigger")
                                    }
                                    // Add other service handlers as needed
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

@Composable
fun ServiceCard(
    service: Service,
    onClick: () -> Unit,
) {
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
                // Icon with peony background
                Box(
                    modifier = Modifier
                        .size(56.dp)
                        .clip(RoundedCornerShape(12.dp))
                        .background(Peony),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = service.icon,
                        contentDescription = service.name,
                        tint = Color.White,
                        modifier = Modifier.size(28.dp)
                    )
                }

                Spacer(modifier = Modifier.width(16.dp))

                // Service info
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = service.name,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = Graphite
                    )

                    Spacer(modifier = Modifier.height(4.dp))

                    Text(
                        text = service.description,
                        fontSize = 14.sp,
                        color = Graphite.copy(alpha = 0.7f),
                        maxLines = 2
                    )
                }

                // Chevron indicator
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