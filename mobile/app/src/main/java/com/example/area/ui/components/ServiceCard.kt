package com.example.area.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.area.data.models.Service
import com.example.area.ui.theme.*

@Composable
fun ServiceCard(
    service: Service,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val icon = getServiceIcon(service.name)
    val description = getServiceDescription(service.name)

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
                ServiceIcon(
                    icon = icon,
                    serviceName = service.name
                )

                Spacer(modifier = Modifier.width(16.dp))
                ServiceInfo(
                    name = service.name,
                    description = description
                )

                ServiceArrow()
            }
        }
    }
}

@Composable
fun ServiceIcon(
    icon: ImageVector,
    serviceName: String,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .size(56.dp)
            .clip(RoundedCornerShape(12.dp))
            .background(Peony),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            imageVector = icon,
            contentDescription = serviceName,
            tint = Color.White,
            modifier = Modifier.size(28.dp)
        )
    }
}

@Composable
fun ServiceInfo(
    name: String,
    description: String,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier) {
        Text(
            text = name,
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
}

@Composable
fun ServiceArrow() {
    Icon(
        Icons.Default.KeyboardArrowRight,
        contentDescription = "Select",
        tint = Peony,
        modifier = Modifier.size(20.dp)
    )
}

fun getServiceIcon(serviceName: String): ImageVector {
    return when (serviceName.lowercase()) {
        "timer", "clock" -> Icons.Default.WatchLater
        "spotify", "music" -> Icons.Default.MusicNote
        "twitch", "stream" -> Icons.Default.OndemandVideo
        "instagram", "facebook", "social" -> Icons.Default.CameraAlt
        "openai", "ai", "chatgpt" -> Icons.Default.Computer
        "notion", "notes" -> Icons.Default.NoteAlt
        "gmail", "email", "outlook" -> Icons.Default.Email
        else -> Icons.Default.Apps
    }
}

fun getServiceDescription(serviceName: String): String {
    return when (serviceName.lowercase()) {
        "timer", "clock" -> "Time-based triggers"
        "spotify" -> "Music and playlist triggers"
        "twitch" -> "Stream and chat triggers"
        "instagram" -> "Post and message triggers"
        "openai" -> "AI-powered triggers"
        "notion" -> "Document and database triggers"
        "gmail" -> "Email-based triggers"
        else -> "${serviceName} triggers"
    }
}