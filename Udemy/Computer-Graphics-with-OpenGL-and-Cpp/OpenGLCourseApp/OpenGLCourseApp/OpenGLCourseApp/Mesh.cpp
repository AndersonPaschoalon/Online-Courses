#include "Mesh.h"

Mesh::Mesh()
{
	this->IBO = 0;
	this->VAO = 0;
	this->VBO = 0;
	this->indexCount = 0;
}

Mesh::~Mesh()
{
	this->clearMesh();
}

void Mesh::createMesh(GLfloat* vertices, unsigned int* indices, unsigned int numOfVertices, unsigned int numOfIndices)
{
	this->indexCount = numOfIndices;

	// Creates the VAO into the GPU
	glGenVertexArrays(1, &this->VAO);
	// Bind the vio to the ID
	glBindVertexArray(this->VAO);

	// ibo buffer
	glGenBuffers(1, &this->IBO);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, this->IBO);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices[0]) * numOfIndices, indices, GL_STATIC_DRAW);

	// Generate the buffer VBO
	glGenBuffers(1, &this->VBO);
	// bind the buffer created to the ID
	glBindBuffer(GL_ARRAY_BUFFER, this->VBO);

	// attach the vertex daa to that VBO
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices[0]) * numOfVertices, vertices, GL_STATIC_DRAW);

	// 3 - the dimensions
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);
	glEnableVertexAttribArray(0);

	glBindBuffer(GL_ARRAY_BUFFER, 0);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
	// importante: you should unbind the ibo/ebo after you unbind the vao. 

	glBindVertexArray(0);


}

void Mesh::renderMesh()
{
	if (this->VAO != 0 && this->IBO != 0 && this->indexCount != 0) 
	{
		glBindVertexArray(this->VAO);
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, this->IBO);

		glDrawElements(GL_TRIANGLES, this->indexCount, GL_UNSIGNED_INT, 0);
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
		glBindVertexArray(0);
	}
}

void Mesh::clearMesh()
{
	if (this->IBO != 0)
	{
		glDeleteBuffers(1, &this->IBO);
		this->IBO = 0;
	}
	if (this->VBO != 0)
	{
		glDeleteBuffers(1, &this->VBO);
		this->VBO = 0;
	}

	if (this->VAO != 0)
	{
		glDeleteVertexArrays(1, &this->VAO);
		this->VAO = 0;
	}

	this->indexCount = 0;
}
