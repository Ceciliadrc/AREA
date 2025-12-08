package com.example.area.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.area.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Preview(showBackground = true)
@Composable
fun ProfileScreen(
    modifier: Modifier = Modifier,
    onBackClick: () -> Unit = {},
    onEditProfile: () -> Unit = {}
) {
    Scaffold(
        topBar = {
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
        },
        containerColor = Color.Transparent
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    brush = Brush.verticalGradient(
                        colors = listOf(Blush, Blossom, Peony)
                    )
                )
                .padding(paddingValues),
            contentAlignment = Alignment.TopCenter
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Spacer(modifier = Modifier.height(40.dp))

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
                        Icons.Default.Person,
                        contentDescription = "Profile",
                        tint = Color.White,
                        modifier = Modifier.size(60.dp)
                    )
                }

                Spacer(modifier = Modifier.height(32.dp))

                ProfileInfoCard(
                    title = "Username",
                    value = "your.email@area.com"
                )

                Spacer(modifier = Modifier.height(24.dp))

                // PUT THE WORKFLOWS STATS DYNAMICALLY
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    StatsCard(
                        title = "Active workflows",
                        value = "2",
                        color1 = Blossom,
                        color2 = Peony,
                        modifier = Modifier.weight(1f)
                    )

                    StatsCard(
                        title = "Workflows executed",
                        value = "23",
                        color1 = Mauve,
                        color2 = Graphite,
                        modifier = Modifier.weight(1f)
                    )
                }

                Spacer(modifier = Modifier.height(40.dp))

                Text(
                    text = "Connected Services",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.White,
                    modifier = Modifier.align(Alignment.Start)
                )

                Spacer(modifier = Modifier.height(16.dp))

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(150.dp)
                        .background(
                            color = Color.White.copy(alpha = 0.2f),
                            shape = MaterialTheme.shapes.medium
                        ),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "Your connected services will appear here",
                        color = Color.White.copy(alpha = 0.7f),
                        fontSize = 14.sp
                    )
                }

                Spacer(modifier = Modifier.height(16.dp))

                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(50.dp)
                        .background(
                            color = Color.White.copy(alpha = 0.2f),
                            shape = MaterialTheme.shapes.medium
                        ),
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
        }
    }
}

@Composable
fun ProfileInfoCard(
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
fun StatsCard(
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
fun BottomNavBar(
    currentRoute: String,
    onWorkflowsClick: () -> Unit,
    onActionsClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier
            .fillMaxWidth()
            .height(80.dp),
        color = Color.Transparent,
        shadowElevation = 8.dp
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Transparent),
            contentAlignment = Alignment.BottomCenter
        ) {
            // Floating Nav Bar Background
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(70.dp)
                    .clip(RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp))
                    .background(
                        brush = Brush.horizontalGradient(
                            colors = listOf(Blossom, Peony, Mauve)
                        )
                    )
            )

            // Navigation Buttons
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(70.dp)
                    .padding(horizontal = 32.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Workflows Button (Left)
                NavButton(
                    icon = Icons.AutoMirrored.Filled.List,
                    label = "Workflows",
                    isSelected = currentRoute == "workflows",
                    onClick = onWorkflowsClick,
                    gradientStart = if (currentRoute == "workflows") Peony else Blossom,
                    gradientEnd = if (currentRoute == "workflows") Mauve else Peony
                )

                // Spacer for center
                Spacer(modifier = Modifier.width(60.dp))

                // Actions Button (Right)
                NavButton(
                    icon = Icons.Default.Add,
                    label = "New Action",
                    isSelected = currentRoute == "actions",
                    onClick = onActionsClick,
                    gradientStart = if (currentRoute == "actions") Peony else Blossom,
                    gradientEnd = if (currentRoute == "actions") Mauve else Peony
                )
            }
        }
    }
}

@Composable
fun NavButton(
    icon: ImageVector,
    label: String,
    isSelected: Boolean,
    onClick: () -> Unit,
    gradientStart: Color,
    gradientEnd: Color,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .width(80.dp)
            .clickable { onClick() },
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Box(
            modifier = Modifier
                .size(if (isSelected) 50.dp else 44.dp)
                .clip(CircleShape)
                .background(
                    Brush.linearGradient(
                        colors = listOf(gradientStart, gradientEnd)
                    )
                    /*if (isSelected) {
                        Brush.linearGradient(
                            colors = listOf(gradientStart, gradientEnd)
                        )
                    } else {
                        Color.Transparent
                    }*/
                ),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = label,
                tint = if (isSelected) Color.White else Color.White.copy(alpha = 0.8f),
                modifier = Modifier.size(if (isSelected) 26.dp else 22.dp)
            )
        }

        Spacer(modifier = Modifier.height(4.dp))

        Text(
            text = label,
            fontSize = 12.sp,
            color = if (isSelected) Color.White else Color.White.copy(alpha = 0.8f),
            fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium
        )
    }
}
