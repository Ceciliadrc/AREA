FROM gradle:8.5-jdk17

RUN apt-get update && \
    apt-get install -y wget unzip && \
    rm -rf /var/lib/apt/lists/*

ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_HOME=${ANDROID_SDK_ROOT}
ENV PATH=${PATH}:${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools

RUN mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O /tmp/sdk.zip && \
    unzip -q /tmp/sdk.zip -d ${ANDROID_SDK_ROOT}/cmdline-tools && \
    mv ${ANDROID_SDK_ROOT}/cmdline-tools/cmdline-tools ${ANDROID_SDK_ROOT}/cmdline-tools/latest && \
    rm /tmp/sdk.zip

RUN yes | sdkmanager --licenses

RUN sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

WORKDIR /app

COPY . .

CMD if [ -f "mobile/gradlew" ]; then \
        cd mobile && \
        chmod +x ./gradlew && \
        ./gradlew assembleDebug --no-daemon --stacktrace --info && \
        mkdir -p /apk && \
        find . -name "*.apk" -type f | head -1 | xargs -I {} cp {} /apk/client.apk && \
        ls -lh /apk/client.apk; \
    elif [ -f "gradlew" ]; then \
        chmod +x ./gradlew && \
        ./gradlew assembleDebug --no-daemon --stacktrace --info && \
        mkdir -p /apk && \
        find . -name "*.apk" -type f | head -1 | xargs -I {} cp {} /apk/client.apk && \
        ls -lh /apk/client.apk; \
    else \
        find . -type f -name "*.gradle*" && \
        exit 1; \
    fi && \
    tail -f /dev/null