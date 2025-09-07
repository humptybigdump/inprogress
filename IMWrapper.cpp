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

#include "stdafx.h"
#include <stdarg.h>

IMWrap::IMWrap()
{
	nAttribs = -1;
	boundShader = 0x7fffffff;

	for ( int i = 0; i < IMWRAP_MAX_VBO; ++i )
		attribName[ i ] = NULL;

	for ( int i = 0; i < IMWRAP_MAX_VBO; i++ )
		history[ i ] = new GLfloat[ IMWRAP_DEFAULT_VERTEX_HISTORY * 4 ];

	historyAllocated = IMWRAP_DEFAULT_VERTEX_HISTORY;

	vaoID = -1;
	glGenVertexArrays( 1, &vaoID );
	glBindVertexArray( vaoID );
	glGenBuffers( IMWRAP_MAX_VBO, vboID );
	glBindVertexArray( 0 );

	_isModified = false;
};

IMWrap::~IMWrap()
{
	glDeleteBuffers( 1, &vaoID );

	for ( int i = 0; i < IMWRAP_MAX_VBO; i++ )
		delete history[ i ];
};


void	IMWrap::Begin( GLenum mode )
{
	_isModified = true;
	_mode = mode;

	// no attribute, no vertices
	attributeUsed = 0;	
	vertexIntermediate = nVertices = 0;	
};

void	IMWrap::End()
{
	int	currentOffset = 3;

	// upload
	glBindVertexArray( vaoID );

	for ( int i = 0; i < nAttribs; i++ )
		if ( attributeUsed & attrFlags[ i ] )
		{
			glBindBuffer( GL_ARRAY_BUFFER, vboID[ i ] );
			glBufferData( GL_ARRAY_BUFFER, 4 * sizeof( GLfloat ) * nVertices, history[ i ], GL_DYNAMIC_DRAW );

			GLint attrLoc = glGetAttribLocation( boundShader, attribName[ i ] );
			if ( attrLoc != -1 )
			{
				glEnableVertexAttribArray( attrLoc );
				glVertexAttribPointer( attrLoc, 4, GL_FLOAT,
									   GL_FALSE, 0, NULL );
			}
		}

	glBindVertexArray( 0 );

	#ifdef IMWRAP_REDUCE_HISTORY_SIZE
	if ( nVertices < historyAllocated / 2 )
	{
		for ( int i = 0; i < IMWRAP_MAX_VBO; i++ )
		{
			GLfloat *historyNew = new GLfloat[ ( nVertices + 1 ) * 4 ];

			memcpy( historyNew, history[ i ], sizeof( GLfloat ) * 4 * nVertices );

			delete history[ i ];

			history[ i ] = historyNew;
		}

		historyAllocated = nVertices + 1;
	}

	#endif
};

void IMWrap::bindShader( const GLhandleARB shader, int _nAttribs, ... )
{
	boundShader = shader;
	nAttribs = _nAttribs;
	va_list names;
	va_start( names, _nAttribs );

	for ( int i = 0; i < _nAttribs; ++i )
	{
		char *n = va_arg( names, char * );

		if ( attribName[ i ] != NULL )
			delete attribName[ i ];

		attribName[ i ] = new char[ strlen( n ) + 1 ];

		strcpy( attribName[ i ], n );
	}

	va_end( names );
}

void IMWrap::bindShaderAttribs( const GLhandleARB shader, int _nAttribs, const char **names )
{
	boundShader = shader;
	nAttribs = _nAttribs;

	for ( int i = 0; i < _nAttribs; ++i )
	{

		if ( attribName[ i ] != NULL )
			delete attribName[ i ];

		attribName[ i ] = new char[ strlen( names[ i ] ) + 1 ];

		strcpy( attribName[ i ], names[ i ] );
	}
}



void	IMWrap::draw()
{
	if ( nAttribs == -1 || boundShader == 0x7fffffff )
	{
		printf( "[WRAP]: no shader binding!\n" );
		return;
	}

	glBindVertexArray( vaoID );

	for ( int i = 0; i < nAttribs; i++ )
		if ( attributeUsed & attrFlags[ i ] )
		{
			glBindBuffer( GL_ARRAY_BUFFER, vboID[ i ] );

			GLint attrLoc = glGetAttribLocation( boundShader, attribName[ i ] );
			if ( attrLoc != -1 )
			{
				glEnableVertexAttribArray( attrLoc );
				glVertexAttribPointer( attrLoc, 4, GL_FLOAT,
									   GL_FALSE, 0, NULL );
			}
		}

	glDrawArrays( _mode, 0, nVertices );
	
	glBindVertexArray( 0 );
	
	glBindBuffer( GL_ARRAY_BUFFER, 0 );

	for ( int i = 0; i < nAttribs; i++ )
		if ( attributeUsed & attrFlags[ i ] )
		{
			GLint attrLoc = glGetAttribLocation( boundShader, attribName[ i ] );
			if ( attrLoc != -1 )
				glDisableVertexAttribArray( attrLoc );
		}
};


