package com.example.area.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.area.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileHeader(
    modifier: Modifier = Modifier,
    onEditProfile: () -> Unit
) {
    TopAppBar(
        title = {
            Text(
                "My profile",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )
        },
        actions = {
            IconButton(onClick = onEditProfile) {
                Icon(Icons.Default.Edit, contentDescription = "Edit Profile")
            }
        },
        colors = TopAppBarDefaults.topAppBarColors(
            containerColor = Color.Transparent,
            titleContentColor = Color.White,
            actionIconContentColor = Color.White,
            navigationIconContentColor = Color.White
        )
    )
}

@Composable
fun ProfileAvatar(
    modifier: Modifier = Modifier,
    size: Int = 120
) {
    Box(
        modifier = modifier
            .size(size.dp)
            .clip(CircleShape)
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(Peony, Mauve)
                )
            ),
        contentAlignment = Alignment.Center
    ) {
        Icon(
            Icons.Default.Person,
            contentDescription = "Profile",
            tint = Color.White,
            modifier = Modifier.size((size * 0.5).dp)
        )
    }
}

@Composable
fun InfoCard(
    title: String,
    value: String,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = Color.White.copy(alpha = 0.9f)
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 20.dp, horizontal = 24.dp)
        ) {
            Text(
                text = title,
                fontSize = 14.sp,
                color = Mauve.copy(alpha = 0.8f),
                fontWeight = FontWeight.Medium
            )

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = value,
                fontSize = 18.sp,
                color = Graphite,
                fontWeight = FontWeight.SemiBold
            )
        }
    }
}

@Composable
fun GradientStatsCard(
    title: String,
    value: String,
    color1: Color,
    color2: Color,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(
            containerColor = Color.Transparent
        ),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(
                    brush = Brush.linearGradient(
                        colors = listOf(color1, color2)
                    ),
                    shape = MaterialTheme.shapes.large
                )
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 24.dp, horizontal = 16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = value,
                    fontSize = 32.sp,
                    color = Color.White,
                    fontWeight = FontWeight.Bold
                )

                Spacer(modifier = Modifier.height(8.dp))

                Text(
                    text = title,
                    fontSize = 14.sp,
                    color = Color.White.copy(alpha = 0.9f),
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }
}

@Composable
fun ServicesSection(
    title: String = "Connected Services",
    isEmpty: Boolean = true,
    onAddService: () -> Unit = {}
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text(
            text = title,
            fontSize = 18.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White,
            modifier = Modifier.align(Alignment.Start)
        )

        if (isEmpty) {
            PlaceholderCard(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(120.dp),
                text = "Your connected services will appear here"
            )

            AddButton(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp),
                onClick = onAddService
            )
        } else {
            // Render connected services list here
            // You can reuse ServiceCard component
        }
    }
}

@Composable
fun PlaceholderCard(
    text: String,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .background(
                color = Color.White.copy(alpha = 0.2f),
                shape = MaterialTheme.shapes.medium
            ),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = text,
            color = Color.White.copy(alpha = 0.7f),
            fontSize = 14.sp
        )
    }
}

@Composable
fun AddButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .background(
                color = Color.White.copy(alpha = 0.2f),
                shape = MaterialTheme.shapes.medium
            )
            .clickable { onClick() },
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = "+",
            color = Color.White.copy(alpha = 0.7f),
            fontSize = 30.sp,
            fontWeight = FontWeight.Bold
        )
    }
}