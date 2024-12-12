#pragma once
#include <stdio.h>
#include <string>
#include <iostream>
#include <fstream>
#include <GL/glew.h>


class Shader
{

public:
	Shader();

	~Shader();

	void createFromString();

	GLuint getProjectionLocation();

	GLuint getModelLocation();

	void useShader();

	void clearShader();


private:
	GLuint shaderID;
	GLuint uniformProjection;
	GLuint uniformModel;

};

