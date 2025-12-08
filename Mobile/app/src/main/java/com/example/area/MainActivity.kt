package com.example.area

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.area.ui.screens.LoginScreen
import com.example.area.ui.screens.ProfileScreen
import com.example.area.ui.screens.WorkflowsScreen
import com.example.area.ui.screens.ActionsScreen
import com.example.area.ui.theme.AreaTheme

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

    // In a real app, you'd use ViewModel + SharedPreferences/Room
    var isLoggedIn by remember { mutableStateOf(false) }

    NavHost(
        navController = navController,
        startDestination = if (isLoggedIn) "profile" else "login",
        modifier = Modifier.fillMaxSize()
    ) {
        // Login Screen
        composable("login") {
            LoginScreen(
                onLoginSuccess = {
                    isLoggedIn = true
                    navController.navigate("profile") {
                        popUpTo("login") { inclusive = true }
                    }
                },
                onNavigateToRegister = {
                    // Navigate to register screen
                    navController.navigate("register")
                }
            )
        }

        // Main Screens (only accessible when logged in)
        composable("profile") {
            ProfileScreen(
                onBackClick = { /* Could exit app or show logout dialog */ },
                onEditProfile = { navController.navigate("editProfile") },
                onNavigateToWorkflows = { navController.navigate("workflows") },
                onNavigateToActions = { navController.navigate("actions") }
            )
        }

        composable("workflows") {
            WorkflowsScreen(
                onBackClick = { navController.navigateUp() },
                onNavigateToProfile = { navController.navigate("profile") },
                onNavigateToActions = { navController.navigate("actions") }
            )
        }

        composable("actions") {
            ActionsScreen(
                onBackClick = { navController.navigateUp() },
                onNavigateToProfile = { navController.navigate("profile") },
                onNavigateToWorkflows = { navController.navigate("workflows") }
            )
        }

        // Other screens (add as needed)
        composable("register") {
            // You'll create this screen
            Text("Register Screen - TODO")
        }

        composable("editProfile") {
            // You'll create this screen
            Text("Edit Profile Screen - TODO")
        }
    }
}

// For logout functionality, add this to your ProfileScreen or create a SettingsScreen:
@Composable
fun handleLogout(navController: NavHostController) {
    // Clear user data/tokens
    // Then navigate back to login
    navController.navigate("login") {
        popUpTo(0) { inclusive = true }
    }
}