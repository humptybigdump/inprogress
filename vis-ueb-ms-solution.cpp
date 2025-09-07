
#include <vector>

#include <math.h>
#include <stddef.h>
#include <stdlib.h>

#include <GL/glut.h>

#ifndef M_PI
#define M_PI		3.141592654f
#endif

#define DRAW_GRID_NODES		1
#define DRAW_GRID_EDGES		1
#define DRAW_GRID_CELLS		1

#define DRAW_MESH_VERTS		1
#define DRAW_MESH_EDGES		1

#define POINT_SIZE			5.0f

#define CELL_COUNT_X		12
#define CELL_COUNT_Y		12

/******************************************************************************/

float Lerp(float a, float b, float t) {
	return a + (b - a) * t;
}

/*******************************************************************************

Mesh data structure

*******************************************************************************/

// A vertex in the edge mesh
struct MeshVertex {
	// Position in world space
	float x, y;
};

// An edge in the edge mesh
struct MeshEdge {
	MeshEdge() {
		vertex0 = vertex1 = NULL;
	}

	// Vertices
	MeshVertex * vertex0, * vertex1;
};

// The edge mesh
class Mesh {
public:
	Mesh() {
	}

private:
	Mesh(Mesh & other);

public:
	~Mesh() {
		for (int i = 0; i < (int) vertices.size(); i++) {
			delete vertices[i];
		}

		for (int i = 0; i < (int) edges.size(); i++) {
			delete edges[i];
		}
	}

private:
	Mesh & operator=(const Mesh &);

public:
	std::vector<MeshVertex *> vertices;
	std::vector<MeshEdge *> edges;
};

/*******************************************************************************

Grid data structure

*******************************************************************************/

// Forward declarations
struct GridCell;

// A node in the uniform grid
struct GridNode {
	GridNode() {
		x = y = 0.0f;
		q = 0.0f;
	}

	// Position in world space
	float x, y;

	// Function value minus isovalue
	float q;
};

// An edge in the uniform grid
struct GridEdge {
	GridEdge() {
		node0 = node1 = NULL;
		cellL = cellR = NULL;
		vertex = NULL;
	}

	GridNode * node0, * node1;
	GridCell * cellL, * cellR;

	// NOTE: We store mesh vertices for easy access during construction
	MeshVertex * vertex;
};

// A cell in the uniform grid
struct GridCell {
	GridCell() {
		nodeBL = nodeBR = nodeTL = nodeTR = NULL;
		edgeB = edgeT = edgeL = edgeR = NULL;
		code = -1;
	}

	GridNode * nodeBL, * nodeBR, * nodeTL, * nodeTR;
	GridEdge * edgeB, * edgeT, * edgeL, * edgeR;

	unsigned char code;
};

// Bounds of the grid in world space
struct GridBounds {
	GridBounds() {
		x0 = -0.8f;
		y0 = -0.8f;
		x1 = +0.8f;
		y1 = +0.8f;
	}
	float x0, y0, x1, y1;
};

// The regular grid
class Grid {
public:
	Grid() {
		cellCountX = cellCountY = 0;
		nodeCountX = nodeCountY = -1;
	}

	void SetSize(int cellCountX, int cellCountY) {
		this->cellCountX = cellCountX;
		this->cellCountY = cellCountY;
		this->nodeCountX = cellCountX + 1;
		this->nodeCountY = cellCountY + 1;

		Free();
		Allocate();

		LinkNodes();
		LinkEdges();
		LinkCells();
	}

private:
	Grid(const Grid &);

public:
	~Grid() {
		Free();
	}

private:
	Grid & operator=(const Grid &);


protected:
	void Allocate() {
		nodes.resize(nodeCountX * nodeCountY);
		for (int i = 0; i < (int) nodes.size(); i++) {
			nodes[i] = new GridNode();
		}

		edges.resize(cellCountX * nodeCountY + nodeCountX * cellCountY);
		for (int i = 0; i < (int) edges.size(); i++) {
			edges[i] = new GridEdge;
		}

		cells.resize(cellCountX * cellCountY);
		for (int i = 0; i < (int) cells.size(); i++) {
			cells[i] = new GridCell();
		}
	}

	void Free() {
		for (int i = 0; i < (int) nodes.size(); i++) {
			delete nodes[i];
		}
		nodes.clear();

		for (int i = 0; i < (int) edges.size(); i++) {
			delete edges[i];
		}
		edges.clear();

		for (int i = 0; i < (int) cells.size(); i++) {
			delete cells[i];
		}
		cells.clear();
	}

	void LinkNodes() {
		int k = 0;
		for (int j = 0; j < nodeCountY; j++) {
			for (int i = 0; i < nodeCountX; i++) {

				float u = (float) i / (float) cellCountX;
				float v = (float) j / (float) cellCountY;

				GridNode * node = new GridNode();

				node->x = Lerp(bounds.x0, bounds.x1, u);
				node->y = Lerp(bounds.y0, bounds.y1, v);

				nodes[k++] = node;
			}
		}
	}

	void LinkEdges() {
		int k = 0;

		// Horizontal edges
		for (int j = 0; j <= cellCountY; j++) {
			for (int i0 = 0, i1 = 1; i0 < cellCountX; i0 = i1++) {
				GridEdge * edge = new GridEdge();

				GridCell * bottom = j > 0          ? cells[i0 + cellCountX * (j - 1)] : NULL;
				GridCell * top    = j < cellCountY ? cells[i0 + cellCountX * (j - 0)] : NULL;

				if (top) {
					top->edgeB = edge;
				}

				if (bottom) {
					bottom->edgeT = edge;
				}

				edge->node0 = nodes[i0 + nodeCountX * j];
				edge->node1 = nodes[i1 + nodeCountX * j];
				edge->cellL = top;
				edge->cellR = bottom;

				edges[k++] = edge;
			}
		}

		// Vertical edges
		for (int j0 = 0, j1 = 1; j0 < cellCountY; j0 = j1++) {
			for (int i = 0; i <= cellCountX; i++) {
				GridEdge * edge = new GridEdge();

				GridCell * left  = i > 0          ? cells[i - 1 + cellCountX * j0] : NULL;
				GridCell * right = i < cellCountX ? cells[i - 0 + cellCountX * j0] : NULL;

				if (left) {
					left->edgeR = edge;
				}

				if (right) {
					right->edgeL = edge;
				}

				edge->node0 = nodes[i + nodeCountX * j0];
				edge->node1 = nodes[i + nodeCountX * j1];
				edge->cellL = left;
				edge->cellR = right;

				edges[k++] = edge;
			}
		}
	}

	void LinkCells() {
		int k = 0;

		for (int j = 0; j < cellCountY; j++) {
			for (int i = 0; i < cellCountX; i++) {
				GridCell * cell = cells[k++];

				int i0 = i;
				int i1 = i0 + 1;
				int j0 = j;
				int j1 = j0 + 1;

				cell->nodeBL = nodes[i0 + nodeCountX * j0];
				cell->nodeTL = nodes[i0 + nodeCountX * j1];
				cell->nodeBR = nodes[i1 + nodeCountX * j0];
				cell->nodeTR = nodes[i1 + nodeCountX * j1];
			}
		}
	}

public:
	GridBounds bounds;

	int cellCountX, cellCountY;
	int nodeCountX, nodeCountY;

	std::vector<GridNode *> nodes;
	std::vector<GridEdge *> edges;
	std::vector<GridCell *> cells;
};


/******************************************************************************/

// Compute Marching Squares for the implicit function f with isovalue c
// Use the grid and output the results in mesh
void MarchingSquares(float (* f)(float x, float y), float c, Grid & grid, Mesh & mesh) {
	// TODO: Implement Macrhing Squares and create edge mesh...

	//...
	//GridNode * node = ...
	//...
	//node->q = f(...) - c;
	//...

	//...
	//MeshVertex * vertex = new MeshVertex();
	//mesh.vertices.push_back(vertex);
	//...

	//...
	//GridCell * cell = ...
	//...
	//cell->code = ...
	//...

	//...
	//MeshEdge * edge = new MeshEdge();
	//edge->vertex0 = ...
	//edge->vertex1 = ...
	//mesh.edges.push_back(edge);
	//...

//SNIP
#if 1

#if 1
	// Compute the node values
	for (int i = 0; i < (int) grid.nodes.size(); i++) {
		GridNode * node = grid.nodes[i];
		node->q = f(node->x, node->y) - c;
	}
#endif

#if 1
	// Create mesh vertices along edges
	for (int i = 0; i < (int) grid.edges.size(); i++) {
		GridEdge * edge = grid.edges[i];

		GridNode * node0 = edge->node0;
		GridNode * node1 = edge->node1;
		float q0 = node0->q;
		float q1 = node1->q;

		// If the signs disagree
		if (q0 * q1 < 0.0f) {
			float x0 = node0->x;
			float y0 = node0->y;

			float x1 = node1->x;
			float y1 = node1->y;

			MeshVertex * vertex = new MeshVertex;

			// Find coordinates by linear interpolation
			// solve for the 0 point between q0 and q1.
			// 0 = a * q0 + (1 - a) * q1
			// from alternative form:
			// x = x0 + (x1 - x0) * [(0 - q0) / (q1 - q0)];
			vertex->x = x0 - (x1 - x0) * q0 / (q1 - q0);
			vertex->y = y0 - (y1 - y0) * q0 / (q1 - q0);

			mesh.vertices.push_back(vertex);

			edge->vertex = vertex;
		}
	}
#endif

#if 1
	// Classify each cell
	for (int i = 0; i < (int) grid.cells.size(); i++) {
		GridCell * cell = grid.cells[i];

		cell->code = 0;
		if (cell->nodeBL->q >= 0.0f) {
			cell->code |= 0x1; // 0001
		}
		if (cell->nodeBR->q >= 0.0f) {
			cell->code |= 0x2; // 0010
		}
		if (cell->nodeTL->q >= 0.0f) {
			cell->code |= 0x4; // 0100
		}
		if (cell->nodeTR->q >= 0.0f) {
			cell->code |= 0x8; // 1000
		}
	}
#endif

#if 1
	// Create the edge mesh from each cell
	for (int i = 0; i < (int) grid.cells.size(); i++) {
		const GridCell * cell = grid.cells[i];

		// Find the right case out of sixteen
		// bit code order for cell nodes:
		// [TR][TL][BR][BL]
		switch (cell->code) {
		case 0x0: // 0000
		case 0xf: // 1111
			// Nothing to do
			break;
		case 0x1: // 0001
		case 0xe: // 1110
			// Edge from left to bottom
			{
				MeshEdge * edge = new MeshEdge();

				edge->vertex0 = cell->edgeL->vertex;
				edge->vertex1 = cell->edgeB->vertex;

				mesh.edges.push_back(edge);
			}
			break;
		case 0x2: // 0010
		case 0xd: // 1101
			// Edge from bottom to right
			{
				MeshEdge * edge = new MeshEdge();

				edge->vertex0 = cell->edgeB->vertex;
				edge->vertex1 = cell->edgeR->vertex;

				mesh.edges.push_back(edge);
			}
			break;
		case 0x3: // 0011
		case 0xc: // 1100
			// Edge from left to right
			{
				MeshEdge * edge = new MeshEdge();

				edge->vertex0 = cell->edgeL->vertex;
				edge->vertex1 = cell->edgeR->vertex;

				mesh.edges.push_back(edge);
			}
			break;
		case 0x4: // 0100
		case 0xb: // 1011
			// Edge from left to top
			{
				MeshEdge * edge = new MeshEdge();

				edge->vertex0 = cell->edgeL->vertex;
				edge->vertex1 = cell->edgeT->vertex;

				mesh.edges.push_back(edge);
			}
			break;
		case 0x5: // 0101
		case 0xa: // 1010
			// Edge from bottom to top
			{
				MeshEdge * edge = new MeshEdge();

				edge->vertex0 = cell->edgeB->vertex;
				edge->vertex1 = cell->edgeT->vertex;

				mesh.edges.push_back(edge);
			}
			break;
		case 0x6: // 0110
		case 0x9: // 1001
			// Ambiguous case
			{
				// Fetch four edge vertices
				MeshVertex * vertex0 = cell->edgeL->vertex;
				MeshVertex * vertex1 = cell->edgeB->vertex;
				MeshVertex * vertex2 = cell->edgeT->vertex;
				MeshVertex * vertex3 = cell->edgeR->vertex;

				// Make sure vertex orders are consistent along both edges
				if (vertex1->x > vertex2->x) {
					// Swap vertices 1 and 2
					MeshVertex * temp = vertex1;
					vertex1 = vertex2;
					vertex2 = temp;
				}

				// Create two edges
				MeshEdge * edge;
				edge = new MeshEdge();
				edge->vertex0 = vertex0;
				edge->vertex1 = vertex1;
				mesh.edges.push_back(edge);

				edge = new MeshEdge();
				edge->vertex0 = vertex2;
				edge->vertex1 = vertex3;
				mesh.edges.push_back(edge);
			}
			break;
		case 0x7: // 0111
		case 0x8: // 1000
			// Edge from top to right
			{
				MeshEdge * edge = new MeshEdge();

				edge->vertex0 = cell->edgeT->vertex;
				edge->vertex1 = cell->edgeR->vertex;

				mesh.edges.push_back(edge);
			}
			break;
		}
	}
#endif

#endif
//SNIP
}

/******************************************************************************/

// Uniform grid
Grid grid;

// Edge mesh
Mesh mesh;

/******************************************************************************/

float Gaussian(float sigma, float r, float rc) {
	r -= rc;
	return 1.0f / (sqrt(2.0f * M_PI) * sigma) * exp(-r * r / (2.0f * sigma * sigma));
}

float Gaussian(float sigma, float x, float y, float xc, float yc, float rc) {
	float r = sqrtf((x - xc) * (x - xc) + (y - yc) * (y - yc));
	return Gaussian(sigma, r, rc);
}

// Simple function to create random floating point numbers in [0, 1)
float RandomFloat() {
	return (float) rand() / (float) (RAND_MAX - 1);
}

/******************************************************************************/

float f(float x, float y) {
	return x * x + y * y;
}

float g(float x, float y) {
	return Gaussian(0.78f, x, y, 0.0f, 0.0f, 0.45f);
}

float h(float x, float y) {
	return sin(x * y * 40) + 0.2f;
}

// Our implicit function
float (* F)(float, float) = h;

// The isovalue
float c = 0.5f;

/******************************************************************************/

void Init() {
	glPointSize(POINT_SIZE);

	grid.SetSize(CELL_COUNT_X, CELL_COUNT_Y);

	MarchingSquares(F, c, grid, mesh);
}

void Exit() {
}

void Keyboard(unsigned char key, int x, int y) {
	if (key == 27) {
		exit(0);
	}
}

void Reshape(int width, int height) {
	glViewport(0, 0, width, height);

	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	if (width > height) {
		glScalef((float) height / (float) width, 1.0f, 1.0f);
	} else {
		glScalef(1.0f, (float) width / (float) height, 1.0f);
	}
}

void Display() {
	// Clear the color buffers
	glClear(GL_COLOR_BUFFER_BIT);

#if DRAW_GRID_CELLS
	// Draw the grid cells
	glBegin(GL_QUADS);
	glColor3ub(8, 45, 49);
	for (int i = 0; i < (int) grid.cells.size(); i++) {
		const GridCell * cell = grid.cells[i];
		glVertex2f(cell->nodeBL->x, cell->nodeBL->y);
		glVertex2f(cell->nodeBR->x, cell->nodeBR->y);
		glVertex2f(cell->nodeTR->x, cell->nodeTR->y);
		glVertex2f(cell->nodeTL->x, cell->nodeTL->y);
	}
	glEnd();
#endif

#if DRAW_GRID_EDGES
	// Draw the grid edges
	glBegin(GL_LINES);
	glColor3ub(255, 211, 78);
	for (int i = 0; i < (int) grid.edges.size(); i++) {
		const GridEdge * edge = grid.edges[i];
		glVertex2f(edge->node0->x, edge->node0->y);
		glVertex2f(edge->node1->x, edge->node1->y);
	}
	glEnd();
#endif

#if DRAW_GRID_NODES
	// Draw the grid nodes
	glBegin(GL_POINTS);
	for (int i = 0; i < (int) grid.nodes.size(); i++) {
		const GridNode * node = grid.nodes[i];
			if (node->q > 0.0f)
				glColor3ub(255, 250, 213);
			else
				glColor3ub(189, 73, 50);
		glVertex2f(node->x, node->y);
	}
	glEnd();
#endif

#if DRAW_MESH_EDGES
	// Draw the mesh edges
	glBegin(GL_LINES);
	glColor3ub(255, 255, 255);
	for (int i = 0; i < (int) mesh.edges.size(); i++) {
		const MeshEdge * edge = mesh.edges[i];
		const MeshVertex * vertex0 = edge->vertex0;
		const MeshVertex * vertex1 = edge->vertex1;
		glVertex2f(vertex0->x, vertex0->y);
		glVertex2f(vertex1->x, vertex1->y);
	}
	glEnd();
#endif

#if DRAW_MESH_VERTS
	// Draw the mesh vertices
	glBegin(GL_POINTS);
	glColor3ub(16, 91, 99);
	for (int i = 0; i < (int) mesh.vertices.size(); i++) {
		const MeshVertex * vertex = mesh.vertices[i];
		glVertex2f(vertex->x, vertex->y);
	}
	glEnd();
#endif

	// Display the result
	glutSwapBuffers();
}

int main(int argc, char ** argv) {
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE);
	glutInitWindowSize(512, 512);
	glutCreateWindow("Marching Squares");

	Init();

	glutKeyboardFunc(&Keyboard);
	glutReshapeFunc(&Reshape);
	glutDisplayFunc(&Display);

	atexit(&Exit);
	glutMainLoop();

	return 0;
}
