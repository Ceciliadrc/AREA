package com.example.area.auth

import android.app.Activity
import android.content.Context
import android.util.Log
import android.widget.Toast
import com.example.area.data.repository.AuthRepository

suspend fun googleAuthFlow(
    context: Context,
    activity: Activity?,
    webClientId: String,
    authRepository: AuthRepository,
    successToast: String,
    onSuccess: () -> Unit
) {
    val safeActivity = activity ?: run {
        Toast.makeText(context, "Google sign-in unavailable", Toast.LENGTH_SHORT).show()
        return
    }

    try {
        val google = GoogleSignInHelper.signIn(safeActivity, webClientId)
        val result = authRepository.loginWithGoogle(
            idToken = google.idToken,
            email = google.email ?: ""
        )

        if (result.isSuccess) {
            Toast.makeText(context, successToast, Toast.LENGTH_SHORT).show()
            onSuccess()
        } else {
            Toast.makeText(context, "Google sign-in failed: ${result.exceptionOrNull()?.message}", Toast.LENGTH_SHORT).show()
        }
    } catch (e: Exception) {
        Toast.makeText(context, "Google sign-in error: ${e.message}", Toast.LENGTH_SHORT).show()
        Log.e("GoogleAuthFlow", "error", e)
    }
}