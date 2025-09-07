/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ render base class
*/

#include "stdafx.h"

#ifndef __RENDER_H
#define __RENDER_H

extern GLFWwindow* glfwWindow;

const int NUM_SAMPLES = 16;

static void APIENTRY debugCallback( GLenum source,
	GLenum type,
	GLuint id,
	GLenum severity,
	GLsizei length,
	const GLchar* message,
	void* userParam )
{
	if ( id != 13 ) // avoid an annoying deprecated warning
		printf( "[DBUG]: %s (%d)\n", message, id );
}


class CRenderBase
{
protected:
	int					width, height;		// height/width of render target
	TextureManager* texMan;
#ifdef USE_SCREEN_LENS
	ScreenLens* lens;
	bool				loadLensShader;
#endif
	GUIFont* font;				// a simple bitmap font output
	bool                offScreenRenderTarget;
	bool				stereoRendering, useMultisampling;
	bool				useAccumulationBuffer;
	float				accumulationEWA;
	bool				enableGLDebugOutput;
	bool				loadTexManShader;
	GLint				textureTarget; // GL_TEXTURE_2D or  GL_TEXTURE_2D_MULTISAMPLE

	GLSLProgram			prgPostProcess;
private:

	GLint				msNumSamples;

	FBOWrapper* fboFramebuffer, * fboPostProcess;
	FBOWrapper* fboFramebuffer3D[ 2 ], * fboPostProcess3D[ 2 ];
	FBOWrapper* fboFrameBufferLastUsed, * fboPostProcessLastUsed;

	IMWrap* wrapAccumulation;
	GLSLProgram			prgDisplayAccumulation;
	int					nImagesAccumulated;
	FBOWrapper* fboAccumulation;

	GLSLProgram			prgAnaglyphStereo;

#ifdef USE_OLD_GLM_OBJ
	GLMmodel* axis;				// the 3d axis model 
#endif

	int					curTime;			// current time for "animation"
	int					lastTimeStamp, fpsCounter, fpsUpdate;
	float				lastFPS;

	IMWrap* wrap, * wrapAnaglyph;

	float				exposure, gamma;

public:
	TrackBall			trackball;

	CRenderBase() : width( 0 ), height( 0 ), curTime( -1 ), fpsCounter( 0 ), fpsUpdate( 20 ), lastFPS( 0.0f ), exposure( 0.0f ), gamma( 1.0f )
	{
		printf( "[RNDR]: starting...\n" );
	#ifdef WIN32
		// some glut32.dll have problems...
		lastTimeStamp = GetTickCount();
	#else
		lastTimeStamp = (int)( glfwGetTime() * 1000.0 );
	#endif
		useAccumulationBuffer = false;
		accumulationEWA = 1.0f;
		nImagesAccumulated = 0;

		useMultisampling = false;
		stereoRendering = false;
		offScreenRenderTarget = false;
		useAccumulationBuffer = false;
		enableGLDebugOutput = false;
	}

	void CRenderBaseInit()
	{
		texMan = new TextureManager();
#ifdef USE_SCREEN_LENS
		lens = new ScreenLens();
		loadLensShader = true;
#endif

		font = new GUIFont( (char*)"./data/font/tahoma12_normal_2x2" );
#ifdef USE_OLD_GLM_OBJ
		axis = glmReadOBJ( (char*)"./data/translator.obj" );
		glmFacetNormals( axis );
#endif

		// hacky: make sure all shaders are loaded in case we need them...
		CRenderBase::loadShaders( true );

		if ( offScreenRenderTarget )
		{
			fboFramebuffer3D[ 0 ] = new FBOWrapper( texMan );
			fboFramebuffer3D[ 1 ] = new FBOWrapper( texMan );
			fboFramebuffer = fboFramebuffer3D[ 0 ];

			fboPostProcess3D[ 0 ] = new FBOWrapper( texMan );
			fboPostProcess3D[ 1 ] = new FBOWrapper( texMan );
			fboPostProcess = fboPostProcess3D[ 0 ];
		}

		if ( useAccumulationBuffer )
			fboAccumulation = new FBOWrapper( texMan );

		loadTexManShader = true;
	}

	void checkSettings()
	{
		if ( enableGLDebugOutput )
		{
			glEnable( GL_DEBUG_OUTPUT );
			glDebugMessageCallback( (GLDEBUGPROC)&debugCallback, NULL );
		} else
			glDisable( GL_DEBUG_OUTPUT );

		if ( useAccumulationBuffer && !offScreenRenderTarget )
		{
			printf( "[RNDR]: accumulation buffer requested, but off-screen rendering disabled!\n" );
			exit( 1 );
		}
		if ( useMultisampling && !offScreenRenderTarget )
		{
			printf( "[RNDR]: multisampling requested, but off-screen rendering disabled!\n" );
			exit( 1 );
		}
		if ( stereoRendering && !offScreenRenderTarget )
		{
			printf( "[RNDR]: stereo rendering requested, but off-screen rendering disabled!\n" );
			exit( 1 );
		}
	}

	~CRenderBase()
	{
		delete texMan;
		delete font;
#ifdef USE_OLD_GLM_OBJ
		delete axis;
#endif
#ifdef USE_SCREEN_LENS
		delete lens;
#endif
	}

	//
	// load 3d models
	//
	virtual	void	loadModels() {};

	//
	// load vertex and fragment shaders
	//
	virtual void	loadShaders( bool firstTime = false )
	{
		if ( offScreenRenderTarget )
		{
			if ( !prgPostProcess.loadVertexShader( (char*)"./glf/shader/postprocess.vp.glsl" ) ||
				 !prgPostProcess.loadFragmentShader( (char*)"./glf/shader/postprocess.fp.glsl" ) )
			{
				if ( firstTime )
					exit( 1 );
			}
			prgPostProcess.link();
			prgPostProcess.parseShaderSetDefault( prgPostProcess.getFragmentShaderSrc() );
			glBindFragDataLocation( prgPostProcess.getProgramObject(), 0, "result" );

			wrap = new IMWrap();
			wrap->bindShader( prgPostProcess.getProgramObject(), 2, "in_position", "in_texcoord" );
			wrap->Begin( GL_TRIANGLES );
			wrap->Attrib2f( 1, 0, 0 );
			wrap->Vertex3f( -1, -1, -0.5f );
			wrap->Attrib2f( 1, 1, 0 );
			wrap->Vertex3f( 1, -1, -0.5f );
			wrap->Attrib2f( 1, 1, 1 );
			wrap->Vertex3f( 1, 1, -0.5f );

			wrap->Attrib2f( 1, 0, 0 );
			wrap->Vertex3f( -1, -1, -0.5f );
			wrap->Attrib2f( 1, 1, 1 );
			wrap->Vertex3f( 1, 1, -0.5f );
			wrap->Attrib2f( 1, 0, 1 );
			wrap->Vertex3f( -1, 1, -0.5f );
			wrap->End();
		}

		if ( stereoRendering )
		{
			if ( !prgAnaglyphStereo.loadVertexShader( (char*)"./glf/shader/anaglyph_stereo.vp.glsl" ) ||
				!prgAnaglyphStereo.loadFragmentShader( (char*)"./glf/shader/anaglyph_stereo.fp.glsl" ) )
			{
				if ( firstTime )
					exit( 1 );
			}

			prgAnaglyphStereo.link();
			glBindFragDataLocation( prgAnaglyphStereo.getProgramObject(), 0, "result" );

			wrapAnaglyph = new IMWrap();
			wrapAnaglyph->bindShader( prgAnaglyphStereo.getProgramObject(), 2, "in_position", "in_texcoord" );
			wrapAnaglyph->Begin( GL_TRIANGLES );
			wrapAnaglyph->Attrib2f( 1, 0, 0 );
			wrapAnaglyph->Vertex3f( -1, -1, -0.5f );
			wrapAnaglyph->Attrib2f( 1, 1, 0 );
			wrapAnaglyph->Vertex3f( 1, -1, -0.5f );
			wrapAnaglyph->Attrib2f( 1, 1, 1 );
			wrapAnaglyph->Vertex3f( 1, 1, -0.5f );

			wrapAnaglyph->Attrib2f( 1, 0, 0 );
			wrapAnaglyph->Vertex3f( -1, -1, -0.5f );
			wrapAnaglyph->Attrib2f( 1, 1, 1 );
			wrapAnaglyph->Vertex3f( 1, 1, -0.5f );
			wrapAnaglyph->Attrib2f( 1, 0, 1 );
			wrapAnaglyph->Vertex3f( -1, 1, -0.5f );
			wrapAnaglyph->End();
		}

		if ( useAccumulationBuffer )
		{
			if ( !prgDisplayAccumulation.loadVertexShader( (char*)"./glf/shader/display_accumulation.vp.glsl" ) ||
				 !prgDisplayAccumulation.loadFragmentShader( (char*)"./glf/shader/display_accumulation.fp.glsl" ) )
			{
				if ( firstTime )
					exit( 1 );
			}

			prgDisplayAccumulation.link();
			glBindFragDataLocation( prgAnaglyphStereo.getProgramObject(), 0, "result" );

			wrapAccumulation = new IMWrap();
			wrapAccumulation->bindShader( prgDisplayAccumulation.getProgramObject(), 2, "in_position", "in_texcoord" );
			wrapAccumulation->Begin( GL_TRIANGLES );
			wrapAccumulation->Attrib2f( 1, 0, 0 );
			wrapAccumulation->Vertex3f( -1, -1, -0.5f );
			wrapAccumulation->Attrib2f( 1, 1, 0 );
			wrapAccumulation->Vertex3f( 1, -1, -0.5f );
			wrapAccumulation->Attrib2f( 1, 1, 1 );
			wrapAccumulation->Vertex3f( 1, 1, -0.5f );

			wrapAccumulation->Attrib2f( 1, 0, 0 );
			wrapAccumulation->Vertex3f( -1, -1, -0.5f );
			wrapAccumulation->Attrib2f( 1, 1, 1 );
			wrapAccumulation->Vertex3f( 1, 1, -0.5f );
			wrapAccumulation->Attrib2f( 1, 0, 1 );
			wrapAccumulation->Vertex3f( -1, 1, -0.5f );
			wrapAccumulation->End();
		}

#ifdef TEXTURE_MANAGER_GUI
		if ( texMan && loadTexManShader )
			texMan->reloadShader();
#endif
#ifdef USE_SCREEN_LENS
		if ( lens && loadLensShader )
			lens->reloadShader();
#endif
	}

	virtual bool	keyboard( int key, int action )
	{
		trackball.keyboard( key, action );
#ifdef USE_SCREEN_LENS
		if ( offScreenRenderTarget )
		lens->keyboard( key, action );
#endif
#ifdef TEXTURE_MANAGER_GUI
		return texMan->keyboard( key, action );
#endif
		return false;
	}

	virtual bool	charCallback( int key )
	{
		return false;
	}

	virtual bool	mouseFunc( int button, int state, int x, int y, int mods )
	{
		return false;
	}

	virtual bool	mouseMotion( int x, int y )
	{
		return false;
	}


	//
	// create textures and render targets
	//
	void	createTextures()
	{
		GLint maxSamples;
		glGetIntegerv( GL_MAX_SAMPLES_EXT, &maxSamples );

		msNumSamples = std::min( maxSamples, NUM_SAMPLES );

		if ( !useMultisampling )
			msNumSamples = -1;

		GLint internalFormat = GL_RGBA32F;

		if ( useMultisampling )
		{
			textureTarget = GL_TEXTURE_2D_MULTISAMPLE;
			internalFormat = GL_RGBA16F;
		} else
			textureTarget = GL_TEXTURE_2D;

		if ( offScreenRenderTarget )
		{
			if ( stereoRendering )
			{
				// stereo render targets
				fboFramebuffer3D[ 0 ]->create( width, height, internalFormat, "Off-Screen RT (left)", GL_DEPTH_COMPONENT24, useMultisampling ? msNumSamples : 0 );
				fboFramebuffer3D[ 1 ]->create( width, height, internalFormat, "Off-Screen RT (right)", GL_DEPTH_COMPONENT24, useMultisampling ? msNumSamples : 0 );

				fboPostProcess3D[ 0 ]->create( width, height, GL_RGBA32F, "Post Process (left)", GL_DEPTH_COMPONENT24 );
				fboPostProcess3D[ 1 ]->create( width, height, GL_RGBA32F, "Post Process (right)", GL_DEPTH_COMPONENT24 );
			} else
			{
				fboFramebuffer3D[ 0 ]->create( width, height, internalFormat, "Off-Screen RT", GL_DEPTH_COMPONENT24, useMultisampling ? msNumSamples : 0 );
				fboPostProcess3D[ 0 ]->create( width, height, GL_RGBA32F, "Post Process", GL_DEPTH_COMPONENT24 );
			}
		}
		if ( useAccumulationBuffer )
			fboAccumulation->create( width, height, GL_RGBA32F, "Accumulation Buffer", GL_DEPTH_COMPONENT24, 0 );
	}

	void	loadCustomPostProcessingShader( const char* vertexShaderFile, const char* fragmentShaderFile, bool firstTime = false )
	{
		if ( !prgPostProcess.loadVertexShader( vertexShaderFile ) ||
			 !prgPostProcess.loadFragmentShader( fragmentShaderFile ) )
		{
			if ( firstTime )
				exit( 1 );
		}
		prgPostProcess.link();

		glBindFragDataLocation( prgPostProcess.getProgramObject(), 0, "result" );
	}

	//
	// prepareOffScreenRendering: prepare everything to render into the off-screen render target
	//                            call this before rendering the scene
	//
	void prepareOffScreenRendering( int monostereo = 0 )
	{
		if ( monostereo == 0 )
			fboFrameBufferLastUsed = fboFramebuffer; else
			fboFrameBufferLastUsed = fboFramebuffer3D[ monostereo - 1 ];
		fboFrameBufferLastUsed->bindUse();
	}

	void prepareOffScreenRenderingPP( int monostereo = 0 )
	{
		if ( monostereo == 0 )
			fboPostProcessLastUsed = fboPostProcess; else
			fboPostProcessLastUsed = fboPostProcess3D[ monostereo - 1 ];
		fboPostProcessLastUsed->bindUse();
	}

	//
	// finishOffScreenRendering: call this after rendering the scene
	//
	void finishOffScreenRendering()
	{
	}

	void finishOffScreenRenderingPP()
	{
	}

	void clearAccumulationBuffer()
	{
		nImagesAccumulated = 0;
	}

	//
	// sceneRender:
	// here we render our scene into the texture bind to the fbo object
	//
	virtual void sceneRender()
	{
		if ( offScreenRenderTarget )
			CRenderBase::prepareOffScreenRendering();

		sceneRenderFrame();

		if ( offScreenRenderTarget )
			CRenderBase::finishOffScreenRendering();

		scenePostProcess();
	}

	virtual void sceneRenderFrame( int invocation = 0 ) {}

	//
	// scenePostProcess():
	// this method is used to post-process the image we generated in 'sceneRender'
	// it draws a textures quad covering the entire window
	// a fragment shader is executed for every pixel
	//

	void setExposureGamma( float e, float g )
	{
		exposure = e;
		gamma = g;
	}

	virtual void scenePostProcess();

	void renderGrid()
	{
		glUseProgram( 0 );
		if ( !useMultisampling )
		{
			glEnable( GL_LINE_SMOOTH );
			glHint( GL_LINE_SMOOTH_HINT, GL_NICEST );
			glEnable( GL_BLEND );
			glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
		}

		glDisable( GL_TEXTURE_2D );
		glLineWidth( 1.0f );
		glBegin( GL_LINES );

		glColor4ub( 0, 0, 0, 255 );
		glVertex3f( -20.0f, 0.0f, 0.0f );
		glVertex3f( +20.0f, 0.0f, 0.0f );
		glVertex3f( 0.0f, 0.0f, -20.0f );
		glVertex3f( 0.0f, 0.0f, +20.0f );

		for ( int i = 1; i < 20; i++ )
		{
			if ( !useMultisampling )
				glColor4ub( 127, 127, 127, 255 ); else
				glColor4ub( 64, 64, 64, 255 );

			glVertex3f( -20.0f, 0.0f, (GLfloat)i );
			glVertex3f( +20.0f, 0.0f, (GLfloat)i );
			glVertex3f( (GLfloat)i, 0.0f, -20.0f );
			glVertex3f( (GLfloat)i, 0.0f, +20.0f );
			glVertex3f( -20.0f, 0.0f, (GLfloat)-i );
			glVertex3f( +20.0f, 0.0f, (GLfloat)-i );
			glVertex3f( (GLfloat)-i, 0.0f, -20.0f );
			glVertex3f( (GLfloat)-i, 0.0f, +20.0f );
		}
		glEnd();
		glDisable( GL_LINE_SMOOTH );
		glDisable( GL_BLEND );

		glPushMatrix();
		glm::vec3 v = trackball.getCameraPosition();
		v += glm::normalize( trackball.getCameraTarget() - v ) * 8.0f;
		v += trackball.getCameraUp() * 2.6f;
		v += trackball.getCameraRight() * 3.6f;
		glTranslatef( v.x, v.y, v.z );
		glScalef( 0.5f, 0.5f, 0.5f );
#ifdef USE_OLD_GLM_OBJ
		glmDraw( axis, GLM_FLAT | GLM_COLOR );
#else
		glLineWidth( 3.0f );
		glBegin( GL_LINES );
		for ( int i = 0; i < 3; i++ )
		{
			glColor3ub( ( i == 0 ) ? 255 : 0, ( i == 1 ) ? 255 : 0, ( i == 2 ) ? 255 : 0 );
			glVertex3f( 0.0f, 0.0f, 0.0f );
			glVertex3f( ( i == 0 ) ? 1.0f : 0.0f, ( i == 1 ) ? 1.0f : 0.0f, ( i == 2 ) ? 1.0f : 0.0f );
		}
		glEnd();
#endif
		glPopMatrix();
	}

	void renderGrid( Camera* cam )
	{
		glMatrixMode( GL_PROJECTION );
		glLoadMatrixf( glm::value_ptr( cam->matP ) );

		glMatrixMode( GL_MODELVIEW );
		glLoadMatrixf( glm::value_ptr( cam->matMV ) );

		glUseProgram( 0 );
		glEnable( GL_LINE_SMOOTH );
		glHint( GL_LINE_SMOOTH_HINT, GL_NICEST );
		glEnable( GL_BLEND );
		glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
		glDisable( GL_TEXTURE_2D );
		glLineWidth( 1.0f );
		glBegin( GL_LINES );

		glColor4ub( 0, 0, 0, 128 );
		glVertex3f( -20.0f, 0.0f, 0.0f );
		glVertex3f( +20.0f, 0.0f, 0.0f );
		glVertex3f( 0.0f, 0.0f, -20.0f );
		glVertex3f( 0.0f, 0.0f, +20.0f );

		for ( int i = 1; i < 20; i++ )
		{
			glColor4ub( 127, 127, 127, 255 );

			glVertex3f( -20.0f, 0.0f, (GLfloat)i );
			glVertex3f( +20.0f, 0.0f, (GLfloat)i );
			glVertex3f( (GLfloat)i, 0.0f, -20.0f );
			glVertex3f( (GLfloat)i, 0.0f, +20.0f );
			glVertex3f( -20.0f, 0.0f, (GLfloat)-i );
			glVertex3f( +20.0f, 0.0f, (GLfloat)-i );
			glVertex3f( (GLfloat)-i, 0.0f, -20.0f );
			glVertex3f( (GLfloat)-i, 0.0f, +20.0f );
		}
		glEnd();
		glDisable( GL_LINE_SMOOTH );
		glDisable( GL_BLEND );

		glPushMatrix();
		glm::vec3 v = cam->camPos;
		v += glm::normalize( cam->camTgt - v ) * 8.0f;
		v += cam->camUp * 2.6f;
		v += cam->camRight * 3.6f;
		glTranslatef( v.x, v.y, v.z );
		glScalef( 0.5f, 0.5f, 0.5f );
#ifdef USE_OLD_GLM_OBJ
		glmDraw( axis, GLM_FLAT | GLM_COLOR );
#else
		glLineWidth( 3.0f );
		glBegin( GL_LINES );
		for ( int i = 0; i < 3; i++ )
		{
			glColor3ub( ( i == 0 ) ? 255 : 0, ( i == 1 ) ? 255 : 0, ( i == 2 ) ? 255 : 0 );
			glVertex3f( 0.0f, 0.0f, 0.0f );
			glVertex3f( ( i == 0 ) ? 1.0f : 0.0f, ( i == 1 ) ? 1.0f : 0.0f, ( i == 2 ) ? 1.0f : 0.0f );
		}
		glEnd();
#endif
		glPopMatrix();
	}

	void	renderNicePoint( glm::vec3 p, glm::vec3 c, float s )
	{
		glEnable( GL_POINT_SMOOTH );
		glEnable( GL_ALPHA_TEST );
		glAlphaFunc( GL_GREATER, 0.25f );
		glColor3fv( &c[ 0 ] );
		glPointSize( s );
		glBegin( GL_POINTS );
		glVertex3fv( &p[ 0 ] );
		glEnd();
		glDisable( GL_ALPHA_TEST );
		glDisable( GL_POINT_SMOOTH );
	}

	void displayStatistics()
	{
		int w, h;
		glfwGetWindowSize( glfwWindow, &w, &h );
		glViewport( 0, 0, w, h );

		glMatrixMode( GL_PROJECTION );
		glPushMatrix();

		glMatrixMode( GL_MODELVIEW );
		glPushMatrix();

		glEnable( GL_TEXTURE_2D );
		glDisable( GL_DEPTH_TEST );
		glDisable( GL_CULL_FACE );

		// some font output, if we want to
#ifdef WIN32
// some glut32.dll have problems...
		curTime = GetTickCount();
#else
		curTime = (int)( glfwGetTime() * 1000.0 );
#endif

		if ( ++fpsCounter >= fpsUpdate )
		{
			float timeElapsed = (float)curTime - (float)lastTimeStamp;
			if ( timeElapsed < 1.0f )
			{
				fpsUpdate *= 2;
			} else
			{
				lastTimeStamp = curTime;
				lastFPS = (float)fpsCounter * 1000.0f / timeElapsed;
				fpsUpdate = 1 + (int)lastFPS;
				fpsCounter = 0;
				if ( timeElapsed > 1000 )
					fpsUpdate = std::max( 5, fpsUpdate / 2 );
			}
		}

		font->setMatrices();
		char status[ 512 ];
		sprintf( status, "%s @ fps %2.1f", glGetString( GL_RENDERER ), lastFPS );
		font->print( status, 0, 0 );

		glm::vec3 p = trackball.getCameraPosition();
		glm::vec3 t = trackball.getCameraTarget();

		sprintf( status, "camera pos (%1.1f, %1.1f, %1.1f), target (%1.1f, %1.1f, %1.1f)", p.x, p.y, p.z, t.x, t.y, t.z );

#ifdef TEXTURE_MANAGER_GUI
		texMan->showTextures();
#endif

#ifdef USE_SCREEN_LENS
		if ( useAccumulationBuffer )
		{
			if ( accumulationEWA < 1.0f || nImagesAccumulated == 0 )
				lens->showLens( fboAccumulation->getTexture( 0 ), false, 1.0f ); else
				lens->showLens( fboAccumulation->getTexture( 0 ), false, 1.0f / (float)std::max( 1, nImagesAccumulated ) ); 
		} else
		{
			if ( offScreenRenderTarget )
				lens->showLens( fboPostProcess->getTexture( 0 ), useMultisampling, 1.0f );
		}
#endif

		glMatrixMode( GL_PROJECTION );
		glPopMatrix();

		glMatrixMode( GL_MODELVIEW );
		glPopMatrix();
	}

	void 	setCameraProjectionAndModelView()
	{
		// setup projection and model view matrix
		glMatrixMode( GL_PROJECTION );
		glLoadIdentity();
		int w, h;
		glfwGetWindowSize( glfwWindow, &w, &h );
		gluPerspective( 45.0f, (float)w / (float)h, 0.1f, 500.0f );

		glMatrixMode( GL_MODELVIEW );
		glLoadIdentity();
		trackball.setupOpenGLMatrix();
	}

};

#endif
