# [STEP 1] build jdk version
FROM eclipse-temurin:21.0.2_13-jdk-jammy AS build
# poit workdir
WORKDIR /home/gradle/project

# cp Gradle (build.gradle, settings.gradle) & Gradle Wrapper
COPY build.gradle settings.gradle gradlew ./
COPY gradle gradle

# Копіюємо вихідний код
COPY src src

RUN chmod +x gradlew # exec +x for Gradle Wrapper
RUN ./gradlew clean build # build

# [STEP 2] make apline version for lith weight x2 less
FROM eclipse-temurin:21.0.2_13-jre-alpine

# point workdir
WORKDIR /app

# cp .jar from jdk built process
COPY --from=build /home/gradle/project/build/libs/helloworld.jar helloworld_app.jar

# run app
ENTRYPOINT ["java", "-jar", "helloworld_app.jar"]