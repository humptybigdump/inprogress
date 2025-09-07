/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ bitmap fonts for OpenGL
*/

#include "stdafx.h"

#pragma warning ( disable : 4996 ) 

GUIFont::GUIFont( char *fontname )
{
	char name[ 1024 ];
	strcpy( name, fontname );
	strcat( name, ".xml" );

	FILE *f = fopen( name, "rt" );
	
	char temp[ 1024 ];
	strcpy( temp, "x" );

	memset( charset, 0, sizeof( CHARACTER ) * 256 );

	while ( !feof( f ) )
	{
		while ( strcmp( temp, "<char" ) != 0 )
		{
			fscanf( f, "%s", temp );
			if ( feof( f ) ) goto xmlEOF;
		}

		int t, x, y, w, h;

		// ID
		fscanf( f, "%s", temp );
		sscanf( &temp[ 4 ], "%d", &t );
		unsigned char ID = t;

		// X
		fscanf( f, "%s", temp );
		sscanf( &temp[ 3 ], "%d", &x );

		// Y
		fscanf( f, "%s", temp );
		sscanf( &temp[ 3 ], "%d", &y );

		// WIDTH
		fscanf( f, "%s", temp );
		sscanf( &temp[ 7 ], "%d", &w );

		// HEIGHT
		fscanf( f, "%s", temp );
		sscanf( &temp[ 8 ], "%d", &h );

		charset[ ID ].x = x;
		charset[ ID ].y = y;
		charset[ ID ].w = w;
		charset[ ID ].h = h;
	}
xmlEOF:

	fclose( f );

	strcpy( name, fontname );
	strcat( name, ".tga" );
	f = fopen( name, "rb" );
	fseek( f, 18, SEEK_SET );
	fread( chardata, 1, 256*256*4, f );
	fclose( f );

	glGenTextures( 1, &texID );
	glBindTexture( GL_TEXTURE_2D, texID );
	glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT );
	glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT );
	glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR );
	glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST );

	//gluBuild2DMipmaps( GL_TEXTURE_2D, 4, 256, 256, GL_RGBA, GL_UNSIGNED_BYTE, chardata );
	glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, 256, 256, 0, GL_RGBA, GL_UNSIGNED_BYTE, chardata );
	glGenerateMipmap( GL_TEXTURE_2D );
};

GUIFont::~GUIFont() {};

void GUIFont::test()
{
	glColor4ub( 255, 255, 255, 255 );
	glEnable( GL_BLEND );
	glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
	glEnable( GL_TEXTURE_2D );
	glBindTexture( GL_TEXTURE_2D, texID );

	glBegin( GL_QUADS );
	glTexCoord2f( 0, 0 );
	glVertex2f( 0, 0 );

	glTexCoord2f( 1, 0 );
	glVertex2f( 256, 0 );
	
	glTexCoord2f( 1, 1 );
	glVertex2f( 256, 256 );
	
	glTexCoord2f( 0, 1 );
	glVertex2f( 0, 256 );
	
	glEnd();
}

int GUIFont::getWidth(const char *str )
{
	int width = 0;

	while ( *str != 0 )
	{
		int id = *(str ++);

		width += charset[ id ].w;
	}

	return width;
}

int GUIFont::getHeight(const char *str )
{
	int height = 0;

	while ( *str != 0 )
	{
		int id = *(str ++);

		height = height > charset[ id ].h ? height : charset[ id ].h;
	}

	return height;

}

void GUIFont::print(const char *str, int x, int y )
{
	glColor4ub( 255, 255, 0, 255 );
	glEnable( GL_BLEND );
	glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
	glEnable( GL_TEXTURE_2D );
	glBindTexture( GL_TEXTURE_2D, texID );

	glBegin( GL_QUADS );

	while ( *str != 0 )
	{
		int id = *(str ++);

		float ta, tb, tc, td;
		ta = (float)charset[ id ].x / 256.0f;
		tb = (float)charset[ id ].y / 256.0f;
		tc = ta + (float)charset[ id ].w / 256.0f;
		td = tb + (float)charset[ id ].h / 256.0f;

		glTexCoord2f( ta, tb );
		glVertex2i  ( x, y );

		glTexCoord2f( tc, tb );
		glVertex2i  ( x + charset[ id ].w, y );
		
		glTexCoord2f( tc, td );
		glVertex2i  ( x + charset[ id ].w, y + charset[ id ].h );
		
		glTexCoord2f( ta, td );
		glVertex2i  ( x, y + charset[ id ].h );
		
		x += charset[ id ].w;
	}

	glEnd();
	glDisable( GL_BLEND );
}

void	GUIFont::setMatrices()
{
	glDisable   ( GL_DEPTH_TEST );

	glMatrixMode( GL_PROJECTION );
	glLoadIdentity();
	glMatrixMode( GL_MODELVIEW );
	glLoadIdentity();
	glScalef( 1.0f, -1.0f, 1.0f );
	glTranslatef( -1.0f, -1.0f, 0.0f );
	int w, h;
	glfwGetWindowSize( glfwWindow, &w, &h );
	glScalef( 2.0f / (float)w, 2.0f / (float)h, 1.0f );
}
