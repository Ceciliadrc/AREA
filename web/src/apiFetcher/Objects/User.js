/*
** EPITECH PROJECT, 2025
** PROJECT_MIRROR
** User.js
*/

export default class User {
  constructor(data = {}) {
    this.user_id = data.user_id ?? null;
    this.username = data.username ?? "";
    this.email = data.email ?? "";

    this.permissions = {
      read: data.permissions?.read ?? true,
      create: data.permissions?.create ?? false,
      update: data.permissions?.update ?? false,
      delete: data.permissions?.delete ?? false,
    };
  }

  static fromJson(json) {
    return new User(json);
  }

  toJson() {
    return {
      user_id: this.user_id,
      username: this.username,
      email: this.email,
      permissions: this.permissions,
    };
  }
}
