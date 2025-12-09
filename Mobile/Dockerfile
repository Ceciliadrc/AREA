## FROM maven:3.6.0-jdk-8-alpine
FROM mobiledevops/android-sdk-image:latest

ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$PATH

RUN curl -s "https://get.sdkman.io" | bash
ENV SDKMAN_DIR=/root/.sdkman
ENV PATH=$SDKMAN_DIR/bin:$PATH
RUN bash -c "source $SDKMAN_DIR/bin/sdkman-init.sh && sdk install kotlin && sdk install gradle"

RUN mkdir -p $ANDROID_SDK_ROOT/cmdline-tools && \
    cd $ANDROID_SDK_ROOT/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdline-tools.zip && \
    unzip cmdline-tools.zip && \
    rm cmdline-tools.zip && \
    mv cmdline-tools latest

RUN yes | sdkmanager --licenses && \
    sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

WORKDIR /app

COPY . .

CMD ["tail", "-f", "/dev/null"]
