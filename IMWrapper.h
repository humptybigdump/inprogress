/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ a wrapper to "collect" geometry for VBOs with operations mimicing immediate mode
*/

#ifndef IM_OPENGL_WRAPPER__H
#define IM_OPENGL_WRAPPER__H

#include "stdafx.h"
#include <list>
#include <vector>

#define WRAP_USE_VAOVBO	

#define IMWRAP_MAX_VBO			8

// minimal #vertices for which memory is allocated, für die von vornherein Speicher allokiert wird
#define IMWRAP_DEFAULT_VERTEX_HISTORY	(1024)

// reduce temporary memory according to simple heuristic
// das sinnvoll erscheint
#define IMWRAP_REDUCE_HISTORY_SIZE

// flags which attributes are used in a batch
#define IMWRAP_ATTR_0			1
#define IMWRAP_ATTR_1			2
#define IMWRAP_ATTR_2			4
#define IMWRAP_ATTR_3			8
#define IMWRAP_ATTR_4			16
#define IMWRAP_ATTR_5			32
#define IMWRAP_ATTR_6			64
#define IMWRAP_ATTR_7			128

const int attrFlags[] = {
    IMWRAP_ATTR_0,
    IMWRAP_ATTR_1,
    IMWRAP_ATTR_2,
    IMWRAP_ATTR_3,
    IMWRAP_ATTR_4,
    IMWRAP_ATTR_5,
    IMWRAP_ATTR_6,
    IMWRAP_ATTR_7
};


class IMWrap {

	protected:
		int	attributeUsed;
		int	nVertices;

		// Die Anzahl und Liste der Vertices dieses Batches
		GLfloat	*history[ IMWRAP_MAX_VBO ];
		int	historyAllocated;

		int	vertexIntermediate;

		GLuint	vaoID, vboID[ IMWRAP_MAX_VBO ];

		// Diese Methode vergrößert bei Bedarf den temporären Speicher
		void	updateCounters();

		bool	_isModified;
		GLenum	_mode;

		GLhandleARB boundShader;
		int nAttribs;
		char *attribName[ IMWRAP_MAX_VBO ];

	protected:

	public:
		IMWrap();

		~IMWrap();

		void bindShader( const GLhandleARB shader, int _nAttribs, ... );
		void bindShaderAttribs( const GLhandleARB shader, int _nAttribs, const char **names );

		void	Begin( GLenum mode = GL_TRIANGLES );
		void	End();

		virtual void	draw();

		bool	isModified() { return _isModified; };

		void	setModified( bool m ) { _isModified = m; };

		void emitVertex() {
			nVertices ++;
			updateCounters();
		};

		__inline void	Attrib4f( int n, GLfloat x, GLfloat y, GLfloat z, GLfloat w )
		{
			attributeUsed |= attrFlags[ n ];
			history[ n ][ nVertices * 4 + 0 ] = x;
			history[ n ][ nVertices * 4 + 1 ] = y;
			history[ n ][ nVertices * 4 + 2 ] = z;
			history[ n ][ nVertices * 4 + 3 ] = w;
		}

		__inline void	Attrib3f( int n, GLfloat x, GLfloat y, GLfloat z )
		{
			attributeUsed |= attrFlags[ n ];
			history[ n ][ nVertices * 4 + 0 ] = x;
			history[ n ][ nVertices * 4 + 1 ] = y;
			history[ n ][ nVertices * 4 + 2 ] = z;
			history[ n ][ nVertices * 4 + 3 ] = 1.0f;
		}

		__inline void	Attrib2f( int n, GLfloat x, GLfloat y )
		{
			attributeUsed |= attrFlags[ n ];
			history[ n ][ nVertices * 4 + 0 ] = x;
			history[ n ][ nVertices * 4 + 1 ] = y;
			history[ n ][ nVertices * 4 + 2 ] = 0.0f;
			history[ n ][ nVertices * 4 + 3 ] = 1.0f;
		}

		__inline void	Attrib4fv( int n, GLfloat *v )
		{
			attributeUsed |= attrFlags[ n ];
			history[ n ][ nVertices * 4 + 0 ] = v[ 0 ];
			history[ n ][ nVertices * 4 + 1 ] = v[ 1 ];
			history[ n ][ nVertices * 4 + 2 ] = v[ 2 ];
			history[ n ][ nVertices * 4 + 3 ] = v[ 3 ];
		}

		__inline void	Attrib3fv( int n, GLfloat *v )
		{
			attributeUsed |= attrFlags[ n ];
			history[ n ][ nVertices * 4 + 0 ] = v[ 0 ];
			history[ n ][ nVertices * 4 + 1 ] = v[ 1 ];
			history[ n ][ nVertices * 4 + 2 ] = v[ 2 ];
			history[ n ][ nVertices * 4 + 3 ] = 1.0f;
		}

		__inline void	Attrib2fv( int n, GLfloat *v )
		{
			attributeUsed |= attrFlags[ n ];
			history[ n ][ nVertices * 4 + 0 ] = v[ 0 ];
			history[ n ][ nVertices * 4 + 1 ] = v[ 1 ];
			history[ n ][ nVertices * 4 + 2 ] = 0.0f;
			history[ n ][ nVertices * 4 + 3 ] = 1.0f;
		}


		__inline void	Vertex4f( GLfloat x, GLfloat y, GLfloat z, GLfloat w )
		{
			Attrib4f( 0, x, y, z, w );
			emitVertex();
		}

		__inline void	Vertex3f( GLfloat x, GLfloat y, GLfloat z )
		{
			Attrib3f( 0, x, y, z );
			emitVertex();
		}

		__inline void	Vertex3fv( GLfloat *p )
		{
			Attrib3f( 0, p[ 0 ], p[ 1 ], p[ 2 ] );
			emitVertex();
		}

		__inline void	Vertex2f( GLfloat x, GLfloat y )
		{
			Attrib2f( 0, x, y );
			emitVertex();
		}
};

inline void	IMWrap::updateCounters() {
	vertexIntermediate ++;

	if ( nVertices == historyAllocated ) {
		// wir benötigen vorraussichtlich mehr Speicher!

		for ( int i = 0; i < IMWRAP_MAX_VBO; i++ ) {
			GLfloat *historyNew = new GLfloat[ historyAllocated * 2 * 4 ];

			memcpy( historyNew, history[ i ], sizeof( GLfloat ) * 4 * historyAllocated );

			delete history[ i ];

			history[ i ] = historyNew;
		}

		historyAllocated *= 2;
	}

	if ( vertexIntermediate == 3 )
		vertexIntermediate = 0;
}


#endif
