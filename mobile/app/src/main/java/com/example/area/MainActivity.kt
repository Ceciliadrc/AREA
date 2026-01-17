package com.example.area

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
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
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.example.area.data.repository.AuthRepository
import com.example.area.ui.screens.*
import com.example.area.ui.theme.*
import com.example.area.ui.components.*

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
@Preview(showBackground = true)
fun AppContent() {
    val navController = rememberNavController()

    var isLoggedIn by remember { mutableStateOf(false) }

    NavHost(
        navController = navController,
        startDestination = if (isLoggedIn) "main" else "login",
        modifier = Modifier.fillMaxSize()
    ) {
        composable("login") {
            LoginScreen(
                onLoginSuccess = {
                    isLoggedIn = true
                    navController.navigate("main") {
                        popUpTo("login") { inclusive = true }
                    }
                },
                onNavigateToRegister = {
                    navController.navigate("register")
                }
            )
        }

        composable("main") {
            val context = androidx.compose.ui.platform.LocalContext.current
            
            MainAppScreen(
                context = context,
                onLogout = {
                    isLoggedIn = false
                    navController.navigate("login") {
                        popUpTo("main") { inclusive = true }
                    }
                }
            )
        }

        composable("register") {
            RegisterScreen(
                onRegisterSuccess = {
                    // After successful registration
                    isLoggedIn = true
                    navController.navigate("main") {
                        popUpTo("register") { inclusive = true }
                    }
                },
                onNavigateToLogin = {
                    navController.navigate("login") {
                        popUpTo("register") { inclusive = true }
                    }
                }
            )
        }
    }
}

@Composable
fun MainAppScreen(
    context: android.content.Context,
    onLogout: () -> Unit
) {
    val innerNavController = rememberNavController()
    val navBackStackEntry by innerNavController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route ?: "profile"
    val authRepository = remember { AuthRepository(context) }

    val showBottomNav = when (currentRoute) {
        "profile", "workflows", "actions" -> true
        else -> false
    }

    Box(modifier = Modifier.fillMaxSize()) {
        NavHost(
            navController = innerNavController,
            startDestination = "profile",
            modifier = Modifier.fillMaxSize()
        ) {
            composable("profile") {
                ProfileScreen(
                    onLogout = {
                        authRepository.logout()
                        onLogout()
                    }
                )
            }

            composable("workflows") {
                WorkflowsScreen()
            }

            composable("actions") {
                ActionScreen()
            }
        }

        if (showBottomNav) {
            Box(
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .fillMaxWidth()
            ) {
                BottomNavBar(
                    currentRoute = currentRoute,
                    onWorkflowsClick = {
                        innerNavController.navigate("workflows") {
                            launchSingleTop = true
                        }
                    },
                    onActionsClick = {
                        innerNavController.navigate("actions") {
                            launchSingleTop = true
                        }
                    },
                    onProfileClick = {
                        innerNavController.navigate("profile") {
                            launchSingleTop = true
                        }
                    }
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
    onProfileClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier
            .fillMaxWidth()
            .height(75.dp),
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
                    .height(80.dp)
                    .clip(RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp))
                    .background(
                        color = Mauve
                    )
            )

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(80.dp)
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

                Spacer(modifier = Modifier.width(60.dp))

                NavButton(
                    icon = Icons.Default.Person,
                    label = "Profile",
                    isSelected = currentRoute == "profile",
                    onClick = onProfileClick,
                    gradientStart = if (currentRoute == "profile") Peony else Blossom,
                    gradientEnd = if (currentRoute == "profile") Mauve else Peony
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
    }
}
