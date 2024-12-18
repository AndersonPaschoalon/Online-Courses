// OpenGLCourseApp.cpp : Este arquivo contém a função 'main'. A execução do programa começa e termina ali.
//
#include <stdio.h>
#include <string.h>
#include <cmath>
#include <GL/glew.h>
#include <GLFW/glfw3.h>
//#include <glm/mat4x4.hpp>
#include <glm/mat4x4.hpp>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

const GLint WIDTH = 800;
const GLint HEIGHT = 600;
const float toRadians = 3.14159265f / 180.0f;

GLuint VAO;
GLuint VBO;
GLuint shader;
GLuint uniformModel;
bool direction = true;
float triOffset = 0.0f;
float triMaxOffset = 0.7f;
float triIncrement = 0.015f;
float currAngle = 0.0f;
float sizeDirection = true;
float currSize = 0.4;
float maxSize = 0.8f;
float minSize = 0.1f;

// vertex shader
static const char* vShader = "\n\
#version 330\n\
\n\
layout (location = 0) in vec3 pos;\n\
\n\
uniform mat4 model;\n\
\n\
void main()\n\
{\n\
	gl_Position = model * vec4(pos, 1.0);\n\
}";

// fragment shader
static const char* fShader = "\n\
#version 330\n\
\n\
out vec4 colour;\n\
\n\
void main()\n\
{\n\
	colour = vec4(1.0, 0.0, 0.0, 1.0);\n\
}";

void AddShader(GLuint theProgram, const char* shaderCode, GLenum shaderType) {
	// create shader
	GLuint  theShader = glCreateShader(shaderType);
	const GLchar* theCode[1];
	theCode[0] = shaderCode;

	GLint codeLenght[1];
	codeLenght[0] = strlen(shaderCode);

	// compile shader
	glShaderSource(theShader, 1, theCode, codeLenght);
	glCompileShader(theShader);

	GLint result = 0;
	GLchar eLog[1024] = { 0 };

	glGetShaderiv(theShader, GL_COMPILE_STATUS, &result);
	if (!result) {
		// print the compile errors
		glGetShaderInfoLog(theShader, sizeof(eLog), NULL, eLog);
		printf("Error compiling the 0x%08x shader: '%s'\n", shaderType,eLog);
		return;
	}

	glAttachShader(theProgram, theShader);

	return;
}

void CompileShaders() {
	// create the program
	shader = glCreateProgram();

	if (!shader) {
		printf("glCreateProgram() ERROR!\n");
		return;
	}

	// Add shader to the program 
	AddShader(shader, vShader, GL_VERTEX_SHADER);
	AddShader(shader, fShader, GL_FRAGMENT_SHADER);

	GLint result = 0;
	GLchar eLog[1024] = { 0 };

	// link the program in the GPU
	glLinkProgram(shader);
	glGetProgramiv(shader, GL_LINK_STATUS, &result);
	if (!result) {
		// print the link errors
		glGetProgramInfoLog(shader, sizeof(eLog), NULL, eLog);
		printf("Error linking program: '%s'\n", eLog);
		return;
	}

	// validate the program
	glValidateProgram(shader);
	glGetProgramiv(shader, GL_VALIDATE_STATUS, &result);
	if (!result) {
		// print the validation errors
		glGetProgramInfoLog(shader, sizeof(eLog), NULL, eLog);
		printf("Error validating program: '%s'\n", eLog);
		return;
	}

	uniformModel = glGetUniformLocation(shader, "model");

}


void CreateTriangle() {
	GLfloat vertices[] = {
		-1.0f, -1.0f, 0.0f,
		1.0f, -1.0f, 0.0f,
		0.0f, 1.0f, 0.0f
	};

	// Creates the VAO into the GPU
	glGenVertexArrays(1, &VAO);
	// Bind the vio to the ID
	glBindVertexArray(VAO);

	// Generate the buffer VBO
	glGenBuffers(1, &VBO);
	// bind the buffer created to the ID
	glBindBuffer(GL_ARRAY_BUFFER, VBO);

	// attach the vertex daa to that VBO
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

	// 3 - the dimensions
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);
	glEnableVertexAttribArray(0);

	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindVertexArray(0);

}



int main()
{
	// Initialize GLFW
	if (!glfwInit()) {
		printf("glfwInit() FAILED\n");
		glfwTerminate();
		return 1;
	}

	// Setup GLFW window properties
	// OpenFL version
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	// Core profile = No backwards compatibility, forward compatibility
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
	glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);

	GLFWwindow* mainWindow = glfwCreateWindow(WIDTH, HEIGHT, "TEXT WINDOW", NULL, NULL);
	if (!mainWindow) {
		printf("glfwCreateWindow() FAILED\n");
		glfwTerminate();
		return 1;
	}

	// Get Buffer size information
	int bufferWidth;
	int bufferHeight;
	glfwGetFramebufferSize(mainWindow, &bufferWidth, &bufferHeight);

	// Set the context for GLEW to use
	glfwMakeContextCurrent(mainWindow);

	// Allow modern extension features
	glewExperimental = GL_TRUE;

	if (glewInit() != GLEW_OK) {
		printf("glewInit() FAILED\n");
		glfwDestroyWindow(mainWindow);
		glfwTerminate();
		return 1;
	}

	// Setup Viewport size
	glViewport(0, 0, bufferWidth, bufferHeight);

	CreateTriangle();
	CompileShaders();


	// Loop until window closed
	while (!glfwWindowShouldClose(mainWindow)) {
		// Get and handle user input events
		glfwPollEvents();

		if (direction) {
			triOffset += triIncrement;
		}
		else {
			triOffset -= triIncrement;
		}
		if (abs(triOffset) >= triMaxOffset) {
			direction = !direction;
		}

		currAngle += 0.5f;
		if (currAngle >= 360) {
			currAngle -= 360; // just to avoid overflow
		}

		if (sizeDirection) {
			currSize += 0.001f;
		}
		else {
			currSize -= 0.001f;
		}

		if (currSize >= maxSize || currSize <= minSize) {
			sizeDirection = !sizeDirection;
		}


		// clear window
		// black
		glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
		// dark gray
		// glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT);

		glUseProgram(shader);

		glm::mat4 model = glm::mat4(1.0f);
		model = glm::translate(model, glm::vec3(triOffset, 0.0f, 0.0f));
		model = glm::rotate(model, currAngle * toRadians, glm::vec3(0.0f, 0.0f, 1.0f));
		model = glm::scale(model, glm::vec3(currSize, currSize, 1.0f));

		glUniformMatrix4fv(uniformModel, 1, GL_FALSE, glm::value_ptr(model));


		glBindVertexArray(VAO);
		// 3 - points we want to  draw
		glDrawArrays(GL_TRIANGLES, 0, 3);
		glBindVertexArray(0);
		

		glUseProgram(0);

		glfwSwapBuffers(mainWindow);
	}



}

