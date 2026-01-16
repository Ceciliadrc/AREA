package com.example.area.ui.screens

import android.text.Layout
import android.util.Log
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import com.example.area.data.repository.RepositoryManager
import com.example.area.data.repository.ServiceRepository
import com.example.area.ui.components.*
import com.example.area.ui.theme.*
import kotlinx.coroutines.launch

@Preview
@Composable
fun ActionScreen(
    modifier: Modifier = Modifier,
    onServiceClick: (com.example.area.data.models.Service) -> Unit = {},
    onTimerClick: () -> Unit = {}
) {
    var services by remember { mutableStateOf<List<com.example.area.data.models.Service>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    val context = LocalContext.current
    val scope = rememberCoroutineScope()

    LaunchedEffect(Unit) {
        scope.launch {
            val serviceRepository = RepositoryManager.getServiceRepository(context)
            val result = serviceRepository.getAllServices()

            isLoading = false

            if (result.isSuccess) {
                services = result.getOrThrow().services
                errorMessage = null
                Log.d("ActionScreen", "Loaded ${services.size} services")
            } else {
                errorMessage = result.exceptionOrNull()?.message
                Log.e("ActionScreen", "Failed to load services: $errorMessage")
            }
        }
    }

    GradientScaffold(
        title = "Choose the trigger",
        modifier = Modifier,
        colors = listOf(Blush, Blossom),
    ) { paddingValues ->
        ServicesListScreen(
            services = services,
            infoTitle = "Available Triggers",
            infoDescription = "Select a service to create an Action. Connect more services in your Profile to unlock additional triggers.",
            isLoading = isLoading,
            errorMessage = errorMessage,
            onRetry = {
                isLoading = true
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
            onServiceClick = { service ->
                when (service.name.lowercase()) {
                    "timer", "clock" -> onTimerClick()
                    else -> onServiceClick(service)
                }
            }
        )
    }
}