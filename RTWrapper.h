/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ FBO wrapper and handling of render targets
*/

#include "stdafx.h"

#ifndef __RTWRAPPER_H
#define __RTWRAPPER_H

#define RT_COLOR0		0x0001
#define RT_COLOR1		0x0002
#define RT_COLOR2		0x0004
#define RT_COLOR3		0x0008
#define RT_COLOR4		0x0010
#define RT_COLOR5		0x0020
#define RT_COLOR6		0x0040
#define RT_COLOR7		0x0080
#define RT_COLOR8		0x0100
#define RT_COLOR9		0x0200
#define RT_COLOR10		0x0400
#define RT_COLOR11		0x0800
#define RT_COLOR12		0x1000
#define RT_COLOR13		0x2000
#define RT_COLOR14		0x4000
#define RT_COLOR15		0x8000
#define RT_VIEWPORT		0x10000

class RTWrapperStack
{
	private:
		typedef struct 
		{ 
			int					flags;
			GLint				colorBuffer[16];
			GLint				viewPort[4];
		} WRAPPER_STATE;

		std::vector<WRAPPER_STATE>	stack;

		int nMaxDrawBuffers;

	protected:
	public:
		RTWrapperStack()
		{
			stack.clear();
			glGetIntegerv( GL_MAX_DRAW_BUFFERS, &nMaxDrawBuffers );
		}; 

		~RTWrapperStack() {};

		void	push( unsigned int flags = 0xffffffff )
		{
			WRAPPER_STATE state;
			memset( &state, 0, sizeof( WRAPPER_STATE ) );
	
			state.flags = flags;

			for ( int i = 1, idx = 0; i <= RT_COLOR15 && idx < nMaxDrawBuffers; i <<= 1, idx++ )
				if ( flags & i )
					glGetIntegerv( GL_DRAW_BUFFER0 + idx, &state.colorBuffer[ idx ] ); 

			if ( flags & RT_VIEWPORT )
				glGetIntegerv( GL_VIEWPORT, state.viewPort );

			stack.push_back( state );		
		};

		void	pop()
		{
			WRAPPER_STATE state = stack.back();

			GLint buffers[16];
			for ( int i = 1, idx = 0; i <= RT_COLOR15 && idx < nMaxDrawBuffers; i <<= 1, idx++ )
				buffers[ idx ] = state.colorBuffer[ idx ]; 

			glDrawBuffers( nMaxDrawBuffers, (GLenum*)buffers );

			if ( state.flags & RT_VIEWPORT )
				glViewport ( state.viewPort[0], state.viewPort[1], state.viewPort[2], state.viewPort[3] );
		};
};

class FBOWrapper
{
private:
	RTWrapperStack RTStack;

	int		msNumSamples;
	int		useMultiSampling;
	int		width, height;

	TextureManager		*texMan;

	FramebufferObject	pFBO;
	Renderbuffer		pRenderBuffer;		// the renderbuffer object we need for having a depth buffer
	OGLTexture			*colorBuffers[ 16 ];
	int					nColorBuffers;

public:
	FBOWrapper( TextureManager *_texMan ) { texMan = _texMan; };
	~FBOWrapper() {};

	int getWidth() { return width; };
	int getHeight() { return height; };

	OGLTexture *getOGLTexture( int idx ) { return colorBuffers[ idx ]; };
	GLint getTexture( int idx ) { return colorBuffers[ idx ]->getID(); };
	FramebufferObject *getFBO() { return &pFBO; };

	void	bindUse()
	{
		RTStack.push();
		pFBO.Bind();

		GLenum buffers[16];
		for ( int i = 0; i < nColorBuffers; i++ )
			buffers[ i ] = GL_COLOR_ATTACHMENT0 + i;

		glDrawBuffers( nColorBuffers, buffers ); 

		glViewport( 0, 0, width, height );
	}

	void	disable()
	{
		pFBO.Disable();
		CheckErrorsGL();
		RTStack.pop();
		CheckErrorsGL();
	}

	bool	create( int _width, int _height, GLint _cbFormat, const char *_cbName, GLint depthFormat, int _useMultiSampling = 0 )
	{
		return create( _width, _height, 1, &_cbFormat, _cbName, depthFormat, _useMultiSampling );
	}

	bool	create( int _width, int _height, int _nColorBuffers, GLint *_cbFormat, const char *_cbName, GLint depthFormat, int _useMultiSampling = 0 )
	{
		width = _width;
		height = _height;
			
		GLint maxSamples;
		glGetIntegerv(GL_MAX_SAMPLES_EXT, &maxSamples);

		msNumSamples = std::min( _useMultiSampling, maxSamples );
		useMultiSampling = msNumSamples > 1;
		if ( !useMultiSampling ) 
			msNumSamples = -1;

		pFBO.Bind();

		nColorBuffers = _nColorBuffers;
		for ( int i = 0; i < nColorBuffers; i++ )
		{
			char name[512];
			if ( _cbName != NULL )
				sprintf( name, "%c", _cbName[ i ] );

			if ( texMan != NULL )
			{
				if ( useMultiSampling )
					texMan->CreateTextureMS( &colorBuffers[ i ], width, height, msNumSamples, _cbFormat[ i ], name ); else
					texMan->CreateTexture( &colorBuffers[ i ], width, height, _cbFormat[ i ], name ); 
			} else
			{
				if ( useMultiSampling )
				{
					colorBuffers[ i ] = new OGLTexture();
					colorBuffers[ i ]->bind();
					colorBuffers[ i ]->createTexture2DMS( width, height, msNumSamples, _cbFormat[ i ] );
					glTexImage2D( GL_TEXTURE_2D_MULTISAMPLE, 0, _cbFormat[ i ], width, height, 0, GL_RGBA, GL_FLOAT, NULL );
				} else
				{
					colorBuffers[ i ] = new OGLTexture();
					colorBuffers[ i ]->bind();
					colorBuffers[ i ]->createTexture2D( width, height, _cbFormat[ i ] );
					glTexImage2D( GL_TEXTURE_2D, 0, _cbFormat[ i ], width, height, 0, GL_RGBA, GL_FLOAT, NULL );
				}
			}

			if ( useMultiSampling )
				pFBO.AttachTexture( GL_TEXTURE_2D_MULTISAMPLE, colorBuffers[ i ]->getID(), GL_COLOR_ATTACHMENT0 + i ); else
				pFBO.AttachTexture( GL_TEXTURE_2D, colorBuffers[ i ]->getID(), GL_COLOR_ATTACHMENT0 + i );
		}
		// initialize depth renderbuffer
		pRenderBuffer.Set( depthFormat, width, height, msNumSamples );
		pFBO.AttachRenderBuffer( pRenderBuffer.GetId(), GL_DEPTH_ATTACHMENT );

		// validate the fbo after attaching textures and render buffers
		pFBO.IsValid();
		pFBO.Disable();

		return true;
	}
};

#endif