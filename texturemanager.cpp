/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ a "texture manager" to browse through textures and render targets in your applications
*/

#include "stdafx.h"

#pragma warning( disable : 4995 )

#include <vector>
using namespace std;

TextureManager::TextureManager()
{
	texEntry.clear();

#ifdef TEXTURE_MANAGER_GUI
	scrollPosition = targetPosition = 0.0f;
	isVisible = 0;
	columns = rows = 2;
	showR = showG = showB = showA = 1;
	exposure = 0.0f;
	showMip = 0;
	showFilter = 0;

	shaderLoaded = false;

	font = new GUIFont( (char *)"./data/font/Bahnschrift" );
	//font = new GUIFont( (char *)"./data/font/aptos" );
	//font = new GUIFont( (char *)"./data/font/tahoma12_normal_2x2" );
	//font = new GUIFont((char*)"./data/font/latha9_normal_2x2");

	int height = font->getHeight( "Ag!/,:" );
	yOfsLine1 = 13 * height / 8;
	yOfsLine2 = 7 * height / 8;
#endif
};

TextureManager::~TextureManager()
{
	std::vector<TM_ENTRY>::iterator	m;

	for ( m = texEntry.begin(); m != texEntry.end(); m++ )
	{
		delete (*m).pTexture;
		(*m).pTexture = 0;
	}			

	texEntry.clear();

	for ( m = texEntryHidden.begin(); m != texEntryHidden.end(); m++ )
	{
		delete (*m).pTexture;
		(*m).pTexture = 0;
	}			

	texEntryHidden.clear();

#ifdef TEXTURE_MANAGER_GUI
	delete font;
#endif
};

void	TextureManager::addEntry( const char *_pSrcFile, OGLTexture *pTexture, bool _show )//, D3DPOOL _pool = D3DPOOL_MANAGED )
{
	TM_ENTRY tmEntry;
	int i;
	for ( i = (int)strlen( _pSrcFile ) - 1; i > 0; i -- )
		if ( _pSrcFile[ i ] == '\\' || _pSrcFile[ i ] == '/' )
			break;
	strcpy( tmEntry.pSrcFile, &_pSrcFile[ (i == 0) ? 0 : (i + 1) ] );
	tmEntry.pTexture  = pTexture;
	tmEntry.show = _show;
	if ( _show )
		texEntry.push_back( tmEntry ); else
		texEntryHidden.push_back( tmEntry );
}

bool	TextureManager::CreateTexture( OGLTexture **ppTexture, int _width, int _height, GLint internalFormat, const char *name, bool _show  ) {
	OGLTexture *pTex = new OGLTexture();
	if ( pTex->createTexture2D( _width, _height, internalFormat ) )
	{
		*ppTexture = pTex;
		addEntry( name, pTex, _show );
		return true;
	}
	return false;
}

bool	TextureManager::CreateTextureMS( OGLTexture **ppTexture, int _width, int _height, int _nSamples, GLint internalFormat, const char *name, bool _show ) {
	OGLTexture *pTex = new OGLTexture();
	if ( pTex->createTexture2DMS( _width, _height, _nSamples, internalFormat ) )
	{
		*ppTexture = pTex;
		addEntry( name, pTex, _show );
		return true;
	}
	return false;
}

bool	TextureManager::CreateTexture2D( OGLTexture **ppTexture, int _width, int _height, GLint internalFormat, GLint sourceFormat, GLint type, void *ptr, const char *name, bool _show ) {
	OGLTexture *pTex = new OGLTexture();
	if ( pTex->createTexture2D( _width, _height, internalFormat ) )
	{
		*ppTexture = pTex;
		addEntry( name, pTex, _show );

		glTexImage2D( GL_TEXTURE_2D, 0, internalFormat, _width, _height, 0, sourceFormat, type, ptr );
		glGenerateMipmap( GL_TEXTURE_2D );
		return true;
	}
	return false;
}

bool	TextureManager::CreateTextureFromTGA( OGLTexture **ppTexture, const char *filename, bool _show ) {
	OGLTexture *pTex = new OGLTexture();
	if ( pTex->loadTGA( filename ) )
	{
		*ppTexture = pTex;
		addEntry( filename, pTex, _show );
		return true;
	} //else
		//printf( "[texture]: problem loading %s.\n", filename );
	return false;
}

bool	TextureManager::CreateTextureFromHDR_RGBE( OGLTexture **ppTexture, const char *filename, bool _show ) {
	OGLTexture *pTex = new OGLTexture();
	if ( pTex->loadHDR_RGBE( filename ) )
	{
		*ppTexture = pTex;
		addEntry( filename, pTex, _show );
		return true;
	} else
		printf( "[texture]: problem loading %s.\n", filename );
	return false;
}

bool	TextureManager::CreateTextureFromHDR( OGLTexture **ppTexture, const char *filename, bool _show ) {
	OGLTexture *pTex = new OGLTexture();
	if ( pTex->loadHDR_FLOAT( filename ) )
	{
		*ppTexture = pTex;
		addEntry( filename, pTex, _show );
		return true;
	} else
		printf( "[texture]: problem loading %s.\n", filename );
	return false;
}

#ifdef TEXTURE_MANAGER_GUI

void TextureManager::reloadShader( bool firstTime )
{
	bool succeded = true;
	if ( !prgRender.loadVertexShader  ( (char*)"./glf/shader/texmanager.vp.glsl" ) ||
 		 !prgRender.loadFragmentShader( (char*)"./glf/shader/texmanager.fp.glsl" ) )
			succeded = false;
	if ( firstTime )
	{
		if ( !succeded )
			exit(1);
	}
	prgRender.link();
	glBindFragDataLocation( prgRender.getProgramObject(), 0, "out_color" );
	shaderLoaded = true;
}

bool	TextureManager::keyboard( int key, int action )  
{
    if( action == GLFW_PRESS )
    {
        switch( key )
        {
			case GLFW_KEY_F10: isVisible = !isVisible; 
				return true;
			case GLFW_KEY_F11: 
			case GLFW_KEY_PAGE_UP: 
				textureManagerScroll = TEXMAN_SCROLL_UP; 
				return true;
			case GLFW_KEY_F12: 
			case GLFW_KEY_PAGE_DOWN: 
				textureManagerScroll = TEXMAN_SCROLL_DOWN; 
				return true;
        }
		if ( isVisible )
		{
			switch( key )
			{
				case '1': columns = 1; rows = 1;	return true;
				case '2': columns = 2; rows = 1;	return true;
				case '3': columns = 3; rows = 1;	return true;
				case '4': columns = 2; rows = 2;	return true;
				case '5': columns = 3; rows = 2;	return true;
				case '6': columns = 3; rows = 2;	return true;
				case '7': columns = 4; rows = 2;	return true;
				case '8': columns = 4; rows = 2;	return true;
				case '9': columns = 4; rows = 3;	return true;
				case '0': columns = 4; rows = 3;	return true;
				case 'R': showR = !showR;			return true;
				case 'G': showG = !showG;			return true;
				case 'B': showB = !showB;			return true;
				case 'A': showA = !showA;			return true;
				case 'F': showFilter = !showFilter;			return true;
				case GLFW_KEY_KP_ADD: case 'U': exposure += 0.1f;		return true;
				case GLFW_KEY_KP_SUBTRACT: case 'J': exposure -= 0.1f;		return true;
				case GLFW_KEY_SPACE: showR = showG = showB = showA = 1; exposure = 0.0f; return true;
				case GLFW_KEY_LEFT: showMip = std::max( 0, showMip - 1 ); return true;
				case GLFW_KEY_RIGHT: showMip = std::min( 16, showMip + 1 ); return true;
			}
		}
    }
	return false;
}

static const char *getNameFromFormat( int format ) {
	// super ugly!
	switch ( format )
	{
		case GL_RGB:			return "RGB"; 
		case GL_RGBA:			return "RGBA"; 
		case GL_RGBA32F:		return "RGBA32F"; 
		case GL_RGBA16F:		return "RGBA16F"; 
		case GL_RGB32F:			return "RGB32F"; 
		case GL_RGB16F:			return "RGB16F"; 
		case GL_RG32F:			return "RG32F"; 
		case GL_RG16F:			return "RG16F"; 
		case GL_R32F:			return "R32F"; 
		case GL_R16F:			return "R16F"; 
		case GL_ALPHA32F_ARB:	return "A32F"; 
		case GL_ALPHA16F_ARB:	return "A16F"; 
		case GL_INTENSITY32F_ARB:	return "Intensity32F"; 
		case GL_LUMINANCE32F_ARB:	return "Luminance32F"; 
		case GL_LUMINANCE_ALPHA32F_ARB:	return "LuminanceAlpha32F"; 
		case GL_INTENSITY16F_ARB:	return "Intensity16F"; 
		case GL_LUMINANCE16F_ARB:	return "Luminance16F"; 
		case GL_LUMINANCE_ALPHA16F_ARB:	return "LuminanceAlpha16F"; 
		default:
			return "unknown format";
	};
}

void	TextureManager::showTextures()
{
	if ( !isVisible ) return;

	if ( !shaderLoaded )
		reloadShader( true );

	int scroll = textureManagerScroll;
	textureManagerScroll = TEXMAN_NO_MORE_SCROLL;


	int w, h;
	glfwGetWindowSize( glfwWindow, &w, &h );
	int modeWidth = w, modeHeight = h;
	w /= columns;
	h /= rows;

	if ( scroll == TEXMAN_SCROLL_DOWN )
		targetPosition = (float)std::max( 0, (int)std::min( (int)(texEntry.size() / columns - 1), (int)(targetPosition + 1) ) );
	if ( scroll == TEXMAN_SCROLL_UP   )
		targetPosition = (float)std::max( 0, (int)std::min( (int)(texEntry.size() / columns - 1), (int)(targetPosition - 1) ) );

	if ( fabsf( targetPosition - scrollPosition ) < 1.1f / (float)h )
		scrollPosition = targetPosition;

	scrollPosition += ( targetPosition - scrollPosition ) * 0.05f;

	int idx = 0;
	std::vector<TM_ENTRY>::iterator	m;

	int destSize = std::min( w, h ) * 70 / 100;
	int firstVisible = (int)floorf( scrollPosition ) * columns;
	int lastVisible = (int)ceilf( scrollPosition + rows ) * columns;

	for ( m = texEntry.begin(); m != texEntry.end(); m++, idx++ )//, idx < start + columns * rows )
	if ( idx >= firstVisible && idx < lastVisible )
	{
		prgRender.bind();
		prgRender.Uniform1i( (char*)"tTexture", 0 );

		rgbaExposure = glm::vec4( (float)showR, (float)showG, (float)showB, (float)showA ) * powf( 2.0f, exposure );


		if ( showR || showG || showB )
			showAlpha = 0; else
			showAlpha = (float)showA;

		prgRender.Uniform4fv( "rgbaExposure", 1, &rgbaExposure[ 0 ]);
		prgRender.Uniform1f( "showAlpha", showAlpha );

		int Width = (*m).pTexture->getWidth(), Height = (*m).pTexture->getHeight();

		glm::vec4 showPosition( (float)( ( idx % columns ) * w ), (float)( ( idx / columns ) * h ), 0.0f, 0.0f );

		glm::vec4 displayParameters( (float)modeWidth, (float)modeHeight, (float)w, (float)h );
		prgRender.Uniform4fv( "displayParameters", 1, &displayParameters[ 0 ] ); 

		showPosition.z  = (float)( destSize * Width / std::max( Width, Height ) );
		showPosition.w  = (float)( destSize * Height / std::max( Width, Height ) );
		showPosition.x += (float)( ( w - destSize ) / 2 + ( destSize - showPosition.z ) / 2 );
		showPosition.y += (float)( ( h - destSize ) / 2 + ( destSize - showPosition.w ) / 2 );
		showPosition.y -= (float)( scrollPosition * h );

		prgRender.Uniform4fv( "showPosition", 1, &showPosition[ 0 ] );
		
		glDisable   ( GL_DEPTH_TEST );
		glDisable  ( GL_CULL_FACE );

		if ( (*m).pTexture->getNSamples() == 0 )
		{
			glEnable( GL_TEXTURE_2D );
			(*m).pTexture->bind();

			GLuint magFilter, minFilter;
			glGetTexParameterIuiv((*m).pTexture->getTarget(), GL_TEXTURE_MAG_FILTER, &magFilter);
			glGetTexParameterIuiv((*m).pTexture->getTarget(), GL_TEXTURE_MIN_FILTER, &minFilter);

			if (showFilter)
			{
				glTexParameterf( (*m).pTexture->getTarget(), GL_TEXTURE_MAG_FILTER, GL_LINEAR );
				glTexParameterf( (*m).pTexture->getTarget(), GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR );
			} else {
				glTexParameterf( (*m).pTexture->getTarget(), GL_TEXTURE_MAG_FILTER, GL_NEAREST );
				glTexParameterf( (*m).pTexture->getTarget(), GL_TEXTURE_MIN_FILTER, GL_NEAREST );
			} 
			float showMipOrig;
			glGetTexParameterfv( (*m).pTexture->getTarget(), GL_TEXTURE_BASE_LEVEL, &showMipOrig );
			glTexParameterf( (*m).pTexture->getTarget(), GL_TEXTURE_BASE_LEVEL, (GLfloat)showMip );

			glBegin( GL_QUADS );
			glVertex2f( 0.0f, 0.0f );
			glVertex2f( 0.0f, 1.0f );
			glVertex2f( 1.0f, 1.0f );
			glVertex2f( 1.0f, 0.0f );
			glEnd();
			glDisable( GL_TEXTURE_2D );

			glTexParameteri((*m).pTexture->getTarget(), GL_TEXTURE_MAG_FILTER, magFilter);
			glTexParameteri((*m).pTexture->getTarget(), GL_TEXTURE_MIN_FILTER, minFilter);
			glTexParameterf( (*m).pTexture->getTarget(), GL_TEXTURE_BASE_LEVEL, (GLfloat)showMipOrig );
		}

		glBindTexture( (*m).pTexture->getTarget(), 0 );
		glUseProgram( 0 );

		showPosition.x = (float)( ( idx % columns ) * w + ( w - destSize ) / 2 );
		showPosition.y = (float)( ( idx / columns ) * h + ( h - destSize ) / 2 );
		showPosition.y -= (float)( scrollPosition * h );

		char	buf[ 256 ], buf2[ 256 ];

		if ( (*m).pTexture->getNSamples() == 0 )
			sprintf( buf, "#%d: '%s', %dx%d", idx, (*m).pSrcFile, Width, Height ); else
			sprintf( buf, "#%d: '%s', %dx%d (MS: %d)", idx, (*m).pSrcFile, Width, Height, (*m).pTexture->getNSamples() ); 
		sprintf( buf2, "%s", getNameFromFormat( (*m).pTexture->getFormat() ) ); 

		glDisable( GL_ALPHA_TEST );
		glDisable ( GL_DEPTH_TEST );
		glDisable ( GL_CULL_FACE );
		font->setMatrices();
		font->print( buf, (int)showPosition.x, (int)showPosition.y - yOfsLine1 );
		font->print( buf2, (int)showPosition.x, (int)showPosition.y - yOfsLine2 );
	}			
	
	char	showInfo[ 512 ];
	if ( showR || showG || showB )
	{
		sprintf( showInfo, "display: color %c%c%c, exposure taps: %2.2f", 
			showR ? 'R' : '.', showG ? 'G' : '.', showB ? 'B' : '.', exposure );
	} else
	{
		sprintf( showInfo, "display: alpha, exposure taps: %2.2f", 
			exposure );
	}
	int textHeight = font->getHeight( showInfo );
	font->print( showInfo, 30, modeHeight - textHeight - 32 );

	font->print( "[1, 2, 3, ..0]  Layout,   R/G/B/A/Space  Channels,   U/J  Exposure,   F  Mip-Mapping on/off,   Left/Right  Mip-Levels", 30, (int)modeHeight - 32 );
}

#endif
