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
GLuint IBO; // index buffer object
GLuint shader;
GLuint uniformModel;
GLuint uniformProjection;
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
out vec4 vColor;\n\
\n\
uniform mat4 model;\n\
uniform mat4 projection;\n\
\n\
void main()\n\
{\n\
	gl_Position = projection * model * vec4(pos, 1.0);\n\
	vColor = vec4(clamp(pos, 0.0f, 1.0f), 1.0f);\n\
}";

// fragment shader
static const char* fShader = "\n\
#version 330\n\
\n\
in vec4 vColor;\n\
\n\
out vec4 colour;\n\
\n\
void main()\n\
{\n\
	colour = vColor;\n\
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
	uniformProjection = glGetUniformLocation(shader, "projection");

}


void CreateTriangle() {
	unsigned int indices[] = {
		0, 3, 1,
		1, 2, 3,
		2, 3, 0,
		0, 1, 2 // base
	};

	GLfloat vertices[] = {
		-1.0f, -1.0f, 0.0f, // bottom left
		0.0f, -1.0f, 1.0f, // background
		1.0f, -1.0f, 0.0f, // bottom right
		0.0f, 1.0f, 0.0f // top
	};

	// Creates the VAO into the GPU
	glGenVertexArrays(1, &VAO);
	// Bind the vio to the ID
	glBindVertexArray(VAO);

	// ibo buffer
	glGenBuffers(1, &IBO);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

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
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
	// importante: you should unbind the ibo/ebo after you unbind the vao. 

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

	// garantir que os triangulos sejam renderizados na profundidade correta
	glEnable(GL_DEPTH_TEST);

	// Setup Viewport size
	glViewport(0, 0, bufferWidth, bufferHeight);

	CreateTriangle();
	CompileShaders();

	glm::mat4 projection = glm::perspective(45.0f, (GLfloat)bufferWidth/(GLfloat)bufferHeight, 0.1f, 100.0f);


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
		glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
		// dark gray
		// glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		glUseProgram(shader);

		glm::mat4 model = glm::mat4(1.0f);
		model = glm::translate(model, glm::vec3(0.0f, triOffset, -2.5f));
		// model = glm::rotate(model, currAngle * toRadians, glm::vec3(0.0f, 1.0f, 1.0f));
		model = glm::scale(model, glm::vec3(0.4f, 0.4f, 1.0f));

		glUniformMatrix4fv(uniformModel, 1, GL_FALSE, glm::value_ptr(model));
		glUniformMatrix4fv(uniformProjection, 1, GL_FALSE, glm::value_ptr(projection));

		glBindVertexArray(VAO);
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO);

		glDrawElements(GL_TRIANGLES, 12, GL_UNSIGNED_INT, 0);
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
		glBindVertexArray(0);
		

		glUseProgram(0);

		glfwSwapBuffers(mainWindow);
	}



}

