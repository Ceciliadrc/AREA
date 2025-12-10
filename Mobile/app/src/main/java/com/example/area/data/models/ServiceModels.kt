package com.example.area.data.models

data class ServicesResponse(
    val services: List<Service>
)

data class Service(
    val id: Int,
    val name: String,
    val displayName: String
)

data class ServiceActionsResponse(
    val serviceId: Int,
    val actions: List<Action>
)

data class Action(
    val id: Int,
    val name: String
)

data class ServiceReactionsResponse(
    val serviceId: Int,
    val reactions: List<Reaction>
)

data class Reaction(
    val id: Int,
    val name: String
)

data class Area(
    val id: Int? = null,
    val name: String,
    val userId: Int,
    val actionId: Int,
    val reactionId: Int
)

data class AreasResponse(
    val userId: Int,
    val username: String,
    val areas: List<AreaDetail>
)

data class AreaDetail(
    val id: Int,
    val name: String,
    val actionId: Int,
    val reactionId: Int
)

data class AboutResponse(
    val client: ClientInfo,
    val server: ServerInfo
)

data class ClientInfo(
    val host: String
)

data class ServerInfo(
    val currentTime: Long,
    val services: List<AboutService>
)

data class AboutService(
    val name: String,
    val actions: List<AboutAction>,
    val reactions: List<AboutReaction>
)

data class AboutAction(
    val name: String,
    val description: String
)

data class AboutReaction(
    val name: String,
    val description: String
)