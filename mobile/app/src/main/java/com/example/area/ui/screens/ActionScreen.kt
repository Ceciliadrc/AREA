package com.example.area.ui.screens

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview

@OptIn(ExperimentalMaterial3Api::class)
@Preview(showBackground = true)
@Composable
fun ActionScreen (
    modifier: Modifier = Modifier,
    onNavigateToWorkflows: () -> Unit = {},
    onNavigateToProfile: () -> Unit = {}
) {}