FROM openjdk:11-jdk-slim
WORKDIR /app
COPY ./build/libs/fat.jar /app/fat.jar
EXPOSE 8080
CMD ["java", "-jar", "/app/fat.jar"]