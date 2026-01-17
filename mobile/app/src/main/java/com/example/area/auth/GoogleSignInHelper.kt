package com.example.area.auth

import android.app.Activity
import android.util.Log
import androidx.credentials.CredentialManager
import androidx.credentials.GetCredentialRequest
import com.google.android.libraries.identity.googleid.GetGoogleIdOption
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential

data class GoogleSignInResult (
    val idToken: String,
    val email: String?,
    val displayName: String?
)

object GoogleSignInHelper {
    private const val TAG = "GoogleSignInHelper"

    suspend fun signIn(activity: Activity, serverClientId: String): GoogleSignInResult {
        val credentialManager = CredentialManager.create(activity)

        val googleIdOption = GetGoogleIdOption.Builder()
            .setServerClientId(serverClientId)
            .setFilterByAuthorizedAccounts(false)
            .setAutoSelectEnabled(false)
            .build()

        val request = GetCredentialRequest.Builder()
            .addCredentialOption(googleIdOption)
            .build()

        val result = credentialManager.getCredential(
            request = request,
            context = activity
        )

        val credential = result.credential
        val googleCred = GoogleIdTokenCredential.createFrom(credential.data)

        Log.d(TAG, "Google sign-in OK: ${googleCred.id}")
        return GoogleSignInResult(
            idToken = googleCred.idToken,
            email = googleCred.id,
            displayName = googleCred.displayName
        )
    }
}