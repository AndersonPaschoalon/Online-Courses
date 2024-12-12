#pragma once

#include <GL/glew.h>


class Mesh
{
public:
	Mesh();
	
	~Mesh();

	/// <summary>
	/// Create the mesh passing all the relevant variables for it.
	/// </summary>
	void createMesh(GLfloat *vertices, unsigned int* indices, unsigned int numOfVertices, unsigned int numOfIndices);

	/// <summary>
	/// Draw the mesh in the screen
	/// </summary>
	void renderMesh();

	/// <summary>
	/// Delete the mesh from the graphic card.
	/// </summary>
	void clearMesh();


private:

	GLuint VAO;
	GLuint VBO;
	GLuint IBO; // index buffer object
	GLsizei indexCount;

};

