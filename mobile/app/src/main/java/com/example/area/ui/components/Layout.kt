package com.example.area.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.area.ui.theme.*

@Composable
fun GradientBackground(
    content: @Composable () -> Unit
) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(Blush, Peony)
                )
            ),
        contentAlignment = Alignment.Center
    ) {
        content()
    }
}

@Composable
fun AuthContainer(
    title: String,
    subtitle: String,
    content: @Composable () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(title, fontSize = 40.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(8.dp))
        Text(subtitle, fontSize = 20.sp, color = Mauve)
        Spacer(modifier = Modifier.height(48.dp))
        content()
    }
}

@Composable
fun OrDivider() {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        HorizontalDivider(
            modifier = Modifier
                .weight(1f)
                .height(2.dp),
            color = Mauve.copy(alpha = 0.5f)
        )
        Text(
            text = "or",
            fontSize = 16.sp,
            color = Mauve,
            modifier = Modifier.padding(horizontal = 16.dp)
        )
        HorizontalDivider(
            modifier = Modifier
                .weight(1f)
                .height(2.dp),
            color = Mauve.copy(alpha = 0.5f)
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GradientScaffold(
    title: String,
    modifier: Modifier = Modifier,
    colors: List<Color> = listOf(Blush, Blossom, Peony),
    content: @Composable (PaddingValues) -> Unit,
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(
                        title,
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold
                    )
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.Transparent,
                    titleContentColor = Color.White
                )
            )
        },
        containerColor = Color.Transparent,
        modifier = modifier
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    brush = Brush.verticalGradient(colors)
                )
                .padding(paddingValues),
            contentAlignment = Alignment.TopCenter
        ) {
            content(paddingValues)
        }
    }
}

@Composable
fun InfoCard(
    title: String,
    description: String,
    stats: String? = null,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier.fillMaxWidth(),
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
        ){
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Icon(
                    Icons.Default.Info,
                    contentDescription = "Info",
                    tint = Peony,
                    modifier = Modifier.size(20.dp)
                )
                Text(
                    text = title,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Graphite
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            Text(
                text = description,
                fontSize = 14.sp,
                color = Graphite.copy(alpha = 0.7f),
                lineHeight = 20.sp
            )

            stats?.let {
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = it,
                    fontSize = 14.sp,
                    color = Peony,
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }
}

@Composable
fun ServicesListScreen(
    services: List<com.example.area.data.models.Service>,
    infoTitle: String,
    infoDescription: String,
    isLoading: Boolean = false,
    errorMessage: String? = null,
    onRetry: () -> Unit = {},
    onServiceClick: (com.example.area.data.models.Service) -> Unit,
    modifier: Modifier = Modifier
) {
    when {
        isLoading -> {
            LoadingState()
        }
        errorMessage != null -> {
            ErrorState(
                title = "Failed to load services",
                message = errorMessage,
                onRetry = onRetry
            )
        }
        services.isEmpty() -> {
            EmptyState(
                icon = {
                    Icon(
                        Icons.Default.Warning,
                        contentDescription = "No Services",
                        tint = Color.White,
                        modifier = Modifier.size(60.dp)
                    )
                },
                title = "No services available",
                message = "The server doesn't have any services configured yet"
            )
        }
        else -> {
            LazyColumn(
                modifier = modifier
                    .fillMaxSize()
                    .padding(horizontal = 24.dp, vertical = 16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                item {
                    InfoCard(
                        title = infoTitle,
                        description = infoDescription,
                        stats = "Services available: ${services.size}"
                    )
                }

                items(services) { service ->
                    ServiceCard(
                        service = service,
                        onClick = { onServiceClick(service) }
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