// OpenGLCourseApp.cpp : Este arquivo contém a função 'main'. A execução do programa começa e termina ali.
//
#include <stdio.h>
#include <string.h>
#include <GL/glew.h>
#include <GLFW/glfw3.h>


const GLint WIDTH = 800;
const GLint HEIGHT = 600;

GLuint VAO;
GLuint VBO;
GLuint shader;

// vertex shader
static const char* vShader = "\n\
#version 330\n\
\n\
layout (location = 0) in vec3 pos;\n\
\n\
void main()\n\
{\n\
	gl_Position = vec4(0.4 * pos.x, 0.6 * pos.y, pos.z, 5.0);\n\
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

		// clear window
		glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
		glClear(GL_COLOR_BUFFER_BIT);

		glUseProgram(shader);

		glBindVertexArray(VAO);
		// 3 - points we want to  draw
		glDrawArrays(GL_TRIANGLES, 0, 3);
		glBindVertexArray(0);
		

		glUseProgram(0);

		glfwSwapBuffers(mainWindow);
	}



}

// Executar programa: Ctrl + F5 ou Menu Depurar > Iniciar Sem Depuração
// Depurar programa: F5 ou menu Depurar > Iniciar Depuração

// Dicas para Começar: 
//   1. Use a janela do Gerenciador de Soluções para adicionar/gerenciar arquivos
//   2. Use a janela do Team Explorer para conectar-se ao controle do código-fonte
//   3. Use a janela de Saída para ver mensagens de saída do build e outras mensagens
//   4. Use a janela Lista de Erros para exibir erros
//   5. Ir Para o Projeto > Adicionar Novo Item para criar novos arquivos de código, ou Projeto > Adicionar Item Existente para adicionar arquivos de código existentes ao projeto
//   6. No futuro, para abrir este projeto novamente, vá para Arquivo > Abrir > Projeto e selecione o arquivo. sln
