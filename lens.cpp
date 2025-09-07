/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ a screen lens for the OpenGL rendering
*/

#include "stdafx.h"

#ifdef USE_SCREEN_LENS

#pragma warning( disable : 4995 )

#include <vector>
using namespace std;

void ScreenLens::reloadShader( bool firstTime )
{
	bool succeeded = true;
	if ( !prgRender.loadVertexShader  ( (char*)"./glf/shader/lens.vp.glsl" ) ||
 		 !prgRender.loadFragmentShader( (char*)"./glf/shader/lens.fp.glsl" ) )
		succeeded = false;
	if ( firstTime && !succeeded )
		exit(1);
	prgRender.link();
	glBindFragDataLocation( prgRender.getProgramObject(), 0, "out_color" );
	shaderLoaded = true;
}

ScreenLens::ScreenLens()
{
	isVisible = 0;
	zoom = 8;
	Width = 320; Height = 240;
	updatePosition = 1;
	first = 1;

	//font = new GUIFont((char*)"./glf/data/font/tahoma12_normal_2x2");
	font = new GUIFont((char*)"./data/font/latha9_normal_2x2");
};

ScreenLens::~ScreenLens()
{
	delete font;
};


bool	ScreenLens::keyboard( int key, int action ) 
{
    if( action == GLFW_PRESS )
    {
        switch( key )
        {
			case GLFW_KEY_F5: isVisible = !isVisible; first = 1;
				return true;
			case GLFW_KEY_F8: updatePosition = !updatePosition; 
				return true;
        }
		if ( isVisible )
		{
			switch( key )
			{
				case GLFW_KEY_F7: 
					zoom *= 2; 
					zoom = std::min( 64, zoom );
					return true;
				case GLFW_KEY_F6: 
					zoom /= 2;
					zoom = std::max( 2, zoom );
					return true;
			}
		}
    }
	return false;
}

static int getQuadrant( int x, int y )
{
	int w, h;
	glfwGetWindowSize( glfwWindow, &w, &h );
	if ( x < w/2 && y < h/2 ) return 0;
	if ( x >= w/2 && y < h/2 ) return 1;
	if ( x < w/2 && y >= h/2 ) return 3;
	//if ( x >= w/2 && y >= h/2 ) 
	return 2;
}

void	ScreenLens::showLens( GLuint texture, bool multisample, float scale )
{
	if ( !isVisible ) return;

	if ( !shaderLoaded )
		reloadShader( true );

	int w, h;
	glfwGetWindowSize( glfwWindow, &w, &h );
	int modeWidth = w, modeHeight = h;

	if ( updatePosition )
		glfwGetCursorPos( glfwWindow, &dx, &dy );

	if ( first )
	{
		first = 0;
		int qMouse = getQuadrant( (int)dx, (int)dy );
		quadrant = ( qMouse + 1 ) % 4;

		posX = (float)( (w/2 - Width)/2 );
		posY = (float)( ((h/2)-Height)/2 );
		if ( quadrant == 1 || quadrant == 2 ) posX += w / 2;
		if ( quadrant == 3 || quadrant == 2 ) posY += h / 2;
		targetX = posX; targetY = posY;
	} else
	if ( updatePosition )
	{
		int qMouse = getQuadrant( (int)dx, (int)dy );

		if ( qMouse == quadrant )
		{
			quadrant = ( qMouse + 1 ) % 4;

			targetX = (float)( (w/2 - Width)/2 );
			targetY = (float)( ((h/2)-Height)/2 );
			if ( quadrant == 1 || quadrant == 2 ) targetX += w / 2;
			if ( quadrant == 3 || quadrant == 2 ) targetY += h / 2;
		}

		if ( fabsf( targetX - posX ) < 1.1f ) posX = targetX;
		if ( fabsf( targetY - posY ) < 1.1f ) posY = targetY;

		posX += ( targetX - posX ) * 0.05f;
		posY += ( targetY - posY ) * 0.05f;
	}

	prgRender.bind();

	prgRender.Uniform1f( "scale", scale );

	glm::vec4 showPosition( (float)( posX ), (float)( posY ), Width, Height );
	
	
	float widthRendertarget = (float)Width / (float)zoom / (float)w;
	float heightRendertarget = (float)Height / (float)zoom / (float)h;

	glm::vec4 readPosition( dx/(float)w - widthRendertarget * 0.5f, 
							dy/(float)h - heightRendertarget * 0.5f, 
							widthRendertarget,
							heightRendertarget );
	prgRender.Uniform4fv( "textureRectangle", 1, &readPosition[ 0 ] ); 

	glm::vec4 displayParameters( (float)w, (float)h, widthRendertarget * (float)w, heightRendertarget * (float)h );
	prgRender.Uniform4fv( "displayParameters", 1, &displayParameters[ 0 ] ); 

	prgRender.Uniform4fv( "showPosition", 1, &showPosition[ 0 ] );
	prgRender.Uniform1i( "zoomValue", zoom );
		
	glDisable   ( GL_DEPTH_TEST );
	glDisable  ( GL_CULL_FACE );
	glDisable( GL_LIGHTING );
	
	glActiveTexture( GL_TEXTURE0 );
	glEnable( GL_TEXTURE_2D );
	glBindTexture( GL_TEXTURE_2D, texture );
	prgRender.Uniform1i( (char*)"tTexture", 0 );

	glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST );
	glTexParameterf( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST );

	glBegin( GL_QUADS );
	glVertex2f( 0.0f, 0.0f );
	glVertex2f( 0.0f, 1.0f );
	glVertex2f( 1.0f, 1.0f );
	glVertex2f( 1.0f, 0.0f );
	glEnd();
	glDisable( GL_TEXTURE_2D );
	glBindTexture( GL_TEXTURE_2D, 0 );
		
	glUseProgram( 0 );

	char	showInfo[ 512 ];
	sprintf( showInfo, "zoom: x%d%s", zoom, updatePosition ? "" : ", fixed pos" );
	
	int textWidth = font->getWidth( showInfo );
	font->print( showInfo, (int)modeWidth - textWidth-20, (int)modeHeight - 32 );
}

#endif