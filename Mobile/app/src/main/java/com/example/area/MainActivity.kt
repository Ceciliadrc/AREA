package com.example.area

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.*
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
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.area.ui.screens.*
import com.example.area.ui.theme.AreaTheme
import com.example.area.ui.theme.Blossom
import com.example.area.ui.theme.Mauve
import com.example.area.ui.theme.Peony

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            AreaTheme {
                AppContent()
            }
        }
    }
}

@Composable
fun AppContent() {
    val navController = rememberNavController()

    var isLoggedIn by remember { mutableStateOf(false) }

    NavHost(
        navController = navController,
        startDestination = if (isLoggedIn) "profile" else "login",
        modifier = Modifier.fillMaxSize()
    ) {
        composable("login") {
            LoginScreen(
                onLoginSuccess = {
                    isLoggedIn = true
                    navController.navigate("profile") {
                        popUpTo("login") { inclusive = true }
                    }
                },
                onNavigateToRegister = {
                    navController.navigate("register")
                }
            )
        }

        composable("profile") {
            ProfileScreen(
                onEditProfile = { navController.navigate("editProfile") },
                onNavigateToWorkflows = { navController.navigate("workflows") },
                onNavigateToActions = { navController.navigate("actions") }
            )
        }

        composable("workflows") {
            WorkflowsScreen(
                onNavigateToProfile = { navController.navigate("profile") },
                onNavigateToActions = { navController.navigate("actions") }
            )
        }

        composable("actions") {
            ActionScreen(
                onNavigateToProfile = { navController.navigate("profile") },
                onNavigateToWorkflows = { navController.navigate("workflows") }
            )
        }

        composable("register") {
            Text("Register Screen - TODO")
        }

        composable("editProfile") {
            Text("Edit Profile Screen - TODO")
        }
    }
}

// Add logout..at some point...somewhere
@Composable
fun handleLogout(navController: NavHostController) {
    navController.navigate("login") {
        popUpTo(0) { inclusive = true }
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

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(70.dp)
                    .padding(horizontal = 32.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                NavButton(
                    icon = Icons.AutoMirrored.Filled.List,
                    label = "Workflows",
                    isSelected = currentRoute == "workflows",
                    onClick = onWorkflowsClick,
                    gradientStart = if (currentRoute == "workflows") Peony else Blossom,
                    gradientEnd = if (currentRoute == "workflows") Mauve else Peony
                )

                Spacer(modifier = Modifier.width(60.dp))

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