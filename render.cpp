/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ render base class and GLFW interfacing
*/

#ifdef _WIN32
// prefer discrete GPU
#ifdef __cplusplus
extern "C" {
#endif

__declspec(dllexport) unsigned int NvOptimusEnablement = 1;
__declspec(dllexport) int AmdPowerXpressRequestHighPerformance = 1;

#ifdef __cplusplus
}
#endif
#endif

#include "stdafx.h"

class CRender;
CRenderBase *pRenderClassBase;

GLFWwindow *glfwWindow;

#define GLFWCALL 

static int running = 1;

const int windowSizeX_initial = 1280;
const int windowSizeY_initial = 768;
int windowSizeX, windowSizeY;

void display()
{
	if ( pRenderClassBase == NULL )	return;

	pRenderClassBase->sceneRender();

	#ifdef USE_TWEAK_BAR
	TwDraw();
	#endif
}

void reshape( GLFWwindow *glfwWindow, int w, int h )
{
	if ( h == 0 ) h = 1;

	glViewport( 0, 0, w, h );

	windowSizeX = w; 
	windowSizeY = h;

	#ifdef USE_TWEAK_BAR
	TwWindowSize( w, h );
	#endif
}

// intialize the application, e.g. call Glew and check for extensions
void _initialize()
{
	glewExperimental = GL_TRUE;
	glewInit();

	#ifdef USE_TWEAK_BAR
	if ( !TwInit( TW_OPENGL, NULL ) )
	{
		fprintf( stderr, "AntTweakBar initialization failed: %s\n", TwGetLastError() );
		exit( 1 );
	}

	int w, h;
	glfwGetWindowSize( glfwWindow, &w, &h );
	TwWindowSize( w, h );
	#endif

	extern void initialize();
	initialize();

	extern CRender *pRenderClass;
	pRenderClassBase = (CRenderBase *)pRenderClass;

	( (CRenderBase *)pRenderClass )->checkSettings();
}

void keyboard( GLFWwindow *glfwWindow, int key, int scancode, int action, int mods )
{
	#ifdef USE_TWEAK_BAR
	if ( TwEventKeyGLFW( key, action ) )
		return;
	#endif
	
	if (action != GLFW_PRESS) return;

	if ( pRenderClassBase == NULL )	return;

	if ( action == GLFW_REPEAT )
		action = GLFW_PRESS;

	if ( pRenderClassBase->keyboard( key, action ) )
		return;

	{
		switch ( key )
		{
			case GLFW_KEY_ESCAPE:
			case 'q':
			case 'Q':
				if ( pRenderClassBase )
					delete pRenderClassBase;
				pRenderClassBase = NULL;
				running = 0;
				break;
			case 'R':
			case 'S':
                if(mods == GLFW_MOD_SHIFT){
                    pRenderClassBase->loadShaders();
                }
				break;
		}
	}
}

void charCallback( GLFWwindow *glfwWindow, unsigned int ch )
{
	if ( pRenderClassBase == NULL )	return;

	if ( pRenderClassBase->charCallback( ch ) )
		return;

	#ifdef USE_TWEAK_BAR
	if ( !TwEventCharGLFW( ch, GLFW_PRESS ) )
	#endif
	{
	}
}

void mousefunc( GLFWwindow *glfwWindow, int button, int state, int mods )
{
	if ( pRenderClassBase == NULL )	return;

	int x, y;
	double dx, dy;
	glfwGetCursorPos( glfwWindow, &dx, &dy );
	x = (int)dx; y = (int)dy;

	#ifdef USE_TWEAK_BAR
	if ( !TwEventMouseButtonGLFW( button, state ) )
	#endif
	{
		//if ( offScreenRenderTarget )
		//{
		//int wx = ( x * windowSizeX_initial ) / windowSizeX;
		//int wy = ( y * windowSizeY_initial ) / windowSizeY;
		int wx = x, wy = y;
		//}

		if ( !pRenderClassBase->mouseFunc( button, state, wx, wy, mods ) )
			pRenderClassBase->trackball.mouseClick( button, state, wx, wy );
	}
}

void mouseWheelFunc( GLFWwindow *glfwWindow, double _x, double _y )
{
	int pos = (int)_y;

	if ( pRenderClassBase == NULL )	return;

	pRenderClassBase->trackball.mouseWheel( pos );
}

void mousemotion( GLFWwindow *glfwWindow, double _x, double _y )
{
	int x = (int)_x;
	int y = (int)_y;

	if ( pRenderClassBase == NULL )	return;

	#ifdef USE_TWEAK_BAR
	if ( !TwEventMousePosGLFW( x, y ) )
		#endif
		if ( !pRenderClassBase->mouseMotion( x, y ) )
			pRenderClassBase->trackball.mouseMotion( x, y );
}

void Terminate()
{
	#ifdef USE_TWEAK_BAR
	TwTerminate();
	#endif
}

#define PRESENTATION_MODEx

int mainProtoGLF( int argc, char **argv )
{
	if ( !glfwInit() )
	{
		fprintf( stderr, "Failed to initialize GLFW\n" );
		exit( EXIT_FAILURE );
	}

	#ifdef PRESENTATION_MODE
	// hide console
	// ShowWindow( GetConsoleWindow(), 0 );
	glfwWindowHint( GLFW_VISIBLE, GL_FALSE );
	glfwWindowHint( GLFW_TRANSPARENT_FRAMEBUFFER, GL_TRUE );
	glfwWindowHint( GLFW_CENTER_CURSOR, GL_TRUE );
	#endif

	glfwWindowHint( GLFW_OPENGL_DEBUG_CONTEXT, GL_FALSE );

	int major = 4, minor = 3;
	glfwWindowHint( GLFW_CONTEXT_VERSION_MAJOR, major );
	glfwWindowHint( GLFW_CONTEXT_VERSION_MINOR, minor );

	if ( major >= 3 )
		glfwWindowHint( GLFW_OPENGL_PROFILE, GLFW_OPENGL_COMPAT_PROFILE );

	glfwWindowHint( GLFW_RED_BITS, 8 );
	glfwWindowHint( GLFW_GREEN_BITS, 8 );
	glfwWindowHint( GLFW_BLUE_BITS, 8 );
	glfwWindowHint( GLFW_ALPHA_BITS, 8 );
	glfwWindowHint( GLFW_STENCIL_BITS, 8 );
	glfwWindowHint( GLFW_DEPTH_BITS, 24 );

	//glfwOpenWindowHint( GLFW_FSAA_SAMPLES, 4 );

	windowSizeX = windowSizeX_initial;
	windowSizeY = windowSizeY_initial;

	glfwWindow = glfwCreateWindow( windowSizeX_initial, windowSizeY_initial, "ProtoGLFW", NULL, NULL );

	if ( glfwWindow == NULL )
	{
		fprintf( stderr, "Failed to open GLFW window\n" );
		glfwTerminate();
		exit( EXIT_FAILURE );
	}

	glfwMakeContextCurrent( glfwWindow );

	extern char applicationTitle[128];
	glfwSetWindowTitle( glfwWindow, applicationTitle );
	//glfwEnable( GLFW_KEY_REPEAT );

	// VSYNC -> set this to 1 (or larger)
	//glfwSwapInterval( 1 );
	glfwSwapInterval( 0 );

	// parse command-line options
	_initialize();

	// set callback functions
	glfwSetWindowSizeCallback( glfwWindow, reshape );
	glfwSetKeyCallback( glfwWindow, keyboard );
	glfwSetCharCallback( glfwWindow, charCallback );
	glfwSetCursorPosCallback( glfwWindow, mousemotion );
	glfwSetMouseButtonCallback( glfwWindow, mousefunc );
	glfwSetScrollCallback( glfwWindow, mouseWheelFunc );

#ifdef PRESENTATION_MODE
	//HWND hwnd = glfwGetWin32Window( glfwWindow );
	//SetWindowLong( hwnd, GWL_STYLE, GetWindowLong( hwnd, GWL_STYLE ) & ~( WS_OVERLAPPEDWINDOW ) );
	/*glfwSetWindowAttrib( glfwWindow, GLFW_FLOATING, GL_TRUE );
	glfwSetWindowAttrib( glfwWindow, GLFW_DECORATED, GL_FALSE );
	glfwSetWindowAttrib( glfwWindow, GLFW_RESIZABLE, GL_FALSE );
	glfwSetWindowAttrib( glfwWindow, GLFW_HOVERED, GL_TRUE );*/
	//glfwSetWindowSize( glfwWindow, 3840, 2160 );
	glfwShowWindow( glfwWindow );
#endif

	// main loop
	while ( !glfwWindowShouldClose( glfwWindow ) && running )
	{
		display();

		glfwSwapBuffers( glfwWindow );
		glfwPollEvents();
	}

	// Terminate GLFW
	glfwTerminate();
#ifdef USE_TWEAK_BAR
	TwTerminate();
#endif

	return 0;
}



void CRenderBase::scenePostProcess()
{
	glBindFramebuffer( GL_READ_FRAMEBUFFER, 0 );
	glBindFramebuffer( GL_DRAW_FRAMEBUFFER, 0 );

	for ( int i = 8; i >= 0; i-- )
	{
		glBindMultiTextureEXT( GL_TEXTURE0 + i, GL_TEXTURE_2D, 0 );
		glBindMultiTextureEXT( GL_TEXTURE0 + i, GL_TEXTURE_2D_MULTISAMPLE, 0 );
	}

	if ( offScreenRenderTarget )
	{
		glDisable( GL_BLEND );
		glEnable( GL_TEXTURE_2D );
		glDisable( GL_DEPTH_TEST );
		glDisable( GL_CULL_FACE );

		// post-process both stereo buffers
		for ( int i = 0; i < ( ( stereoRendering ) ? 2 : 1 ); i++ )
		{
			prepareOffScreenRenderingPP( i + 1 );

			// read from our off-screen render target
			glBindMultiTextureEXT( GL_TEXTURE0_ARB, textureTarget, fboFramebuffer3D[ i ]->getTexture( 0 ) );

			prgPostProcess.bind();
			prgPostProcess.Uniform1i( (char *)"useMultisampling", useMultisampling ? 1 : 0 );
			prgPostProcess.Uniform1i( (char *)"msNumSamples", msNumSamples );
			prgPostProcess.Uniform1i( (char *)"tOffScreenBuffer", 0 );
			prgPostProcess.Uniform1i( (char *)"tOffScreenBufferMS", 0 );
			prgPostProcess.Uniform1i( (char *)"tOffScreenBufferWidth", width );
			prgPostProcess.Uniform1i( (char *)"tOffScreenBufferHeight", height );
			prgPostProcess.Uniform1f( (char *)"exposure", exposure );
			prgPostProcess.Uniform1f( (char *)"gamma", gamma );

			wrap->draw();

			glBindTexture( textureTarget, 0 );

			finishOffScreenRenderingPP();
		}

		if ( stereoRendering )
		{
			if ( useAccumulationBuffer )
			{
				glEnable( GL_BLEND );
				glBlendFunc( GL_ONE, GL_ONE );
				glBlendEquation( GL_FUNC_ADD );

				// accumulate
				fboAccumulation->bindUse();
				if ( nImagesAccumulated == 0 )
				{
					glClearColor( 0.0f, 0.0f, 0.0f, 0.0f );
					glClear( GL_COLOR_BUFFER_BIT );
				}
				nImagesAccumulated ++;
			} else
			{
				glDrawBuffer( GL_BACK );                       // Set the back buffer as the draw buffer
				glBindFramebuffer( GL_READ_FRAMEBUFFER, 0 );
				glBindFramebuffer( GL_DRAW_FRAMEBUFFER, 0 );
			}

			// read from our off-screen render target
			glBindMultiTextureEXT( GL_TEXTURE0_ARB, GL_TEXTURE_2D, fboPostProcess3D[ 0 ]->getTexture( 0 ) );
			glBindMultiTextureEXT( GL_TEXTURE1_ARB, GL_TEXTURE_2D, fboPostProcess3D[ 1 ]->getTexture( 0 ) );

			prgAnaglyphStereo.bind();
			prgAnaglyphStereo.Uniform1i( (char *)"tOffScreenBuffer0", 0 );
			prgAnaglyphStereo.Uniform1i( (char *)"tOffScreenBuffer1", 1 );

			wrapAnaglyph->draw();

			glBindMultiTextureEXT( GL_TEXTURE0_ARB, GL_TEXTURE_2D, 0 );
			glBindMultiTextureEXT( GL_TEXTURE1_ARB, GL_TEXTURE_2D, 0 );

			if ( useAccumulationBuffer )
			{
				fboAccumulation->disable();
				glDisable( GL_BLEND );
				prgDisplayAccumulation.bind();
				glDrawBuffer( GL_BACK );                       // Set the back buffer as the draw buffer
				glBindFramebuffer( GL_READ_FRAMEBUFFER, 0 );
				glBindFramebuffer( GL_DRAW_FRAMEBUFFER, 0 );
				glBindMultiTextureEXT( GL_TEXTURE0_ARB, GL_TEXTURE_2D, fboAccumulation->getTexture( 0 ) );
				prgDisplayAccumulation.Uniform1f( "scale", 1.0f / (float)nImagesAccumulated );
				wrapAccumulation->draw();
			}
		} else
		{
			int w, h;
			glfwGetWindowSize( glfwWindow, &w, &h );

			if ( useAccumulationBuffer )
			{
				glEnable( GL_BLEND );
				
				static float prevAccumulationEWA = -1.0f;

				if ( prevAccumulationEWA != accumulationEWA && accumulationEWA == 1.0f )
					nImagesAccumulated = 0;
				
				prevAccumulationEWA = accumulationEWA;

				if ( accumulationEWA == 1.0f )
					glBlendFunc( GL_ONE, GL_ONE ); else
				{
					glBlendFunc( GL_ONE, GL_CONSTANT_COLOR );
					float c = 1 - accumulationEWA;
					glBlendColor( c, c, c, c );
				}

				glBlendEquation( GL_FUNC_ADD );

				// accumulate
				fboAccumulation->bindUse();

				if ( nImagesAccumulated == 0 )
				{
					glClearColor( 0.0f, 0.0f, 0.0f, 0.0f );
					glClear( GL_COLOR_BUFFER_BIT );
				}

				glBindMultiTextureEXT( GL_TEXTURE0_ARB, GL_TEXTURE_2D, fboPostProcess->getTexture( 0 ) );
				prgDisplayAccumulation.bind();
				if ( accumulationEWA < 1.0f && nImagesAccumulated == 0 )
					prgDisplayAccumulation.Uniform1f( "scale", 1.0f ); else
					prgDisplayAccumulation.Uniform1f( "scale", accumulationEWA );

				wrapAccumulation->draw();
				nImagesAccumulated ++;
				//fboAccumulation->disable();

				glDisable( GL_BLEND );
				
				glBindFramebuffer( GL_READ_FRAMEBUFFER, 0 );
				glBindFramebuffer( GL_DRAW_FRAMEBUFFER, 0 );
				glDrawBuffer( GL_BACK );                       // Set the back buffer as the draw buffer

				glBindMultiTextureEXT( GL_TEXTURE0_ARB, GL_TEXTURE_2D, fboAccumulation->getTexture( 0 ) );

				prgDisplayAccumulation.bind();
				if ( accumulationEWA == 1.0f )
				{
					prgDisplayAccumulation.Uniform1f( "scale", 1.0f / (float)nImagesAccumulated );
				}
				else
					prgDisplayAccumulation.Uniform1f( "scale", 1.0f );

				glViewport( 0, 0, w, h );
				wrapAccumulation->draw();
			} else
			{
				glDisable( GL_BLEND );
				glBindFramebuffer( GL_DRAW_FRAMEBUFFER, 0 );   // Make sure no FBO is set as the draw framebuffer
				glBindFramebuffer( GL_READ_FRAMEBUFFER, fboPostProcess->getFBO()->getID() ); // Make sure your multisampled FBO is the read framebuffer
				glBlitFramebuffer( 0, 0, width, height, 0, 0, w, h, GL_COLOR_BUFFER_BIT, GL_LINEAR );
				glBindFramebuffer( GL_READ_FRAMEBUFFER, 0 );
			}
		}
	}

	// orthogonal projection for rendering the screen quad
	glMatrixMode( GL_PROJECTION );
	glPushMatrix();
	glLoadIdentity();
	glOrtho( -1.0f, 1.0f, -1.0f, 1.0f, 0.0f, 10.0f );

	glMatrixMode( GL_MODELVIEW );
	glPushMatrix();
	glLoadIdentity();

	glUseProgram( 0 );
	displayStatistics();

	glMatrixMode( GL_PROJECTION );
	glPopMatrix();

	glMatrixMode( GL_MODELVIEW );
	glPopMatrix();
}

/*int APIENTRY wWinMain( _In_ HINSTANCE hInstance,
					 _In_opt_ HINSTANCE hPrevInstance,
					 _In_ LPWSTR    lpCmdLine,
					 _In_ int       nCmdShow )
{
	mainProtoGLF( 0, NULL );
	exit( EXIT_SUCCESS );
}*/

int main( int argc, char **argv )
{
	mainProtoGLF( argc, argv );
	exit( EXIT_SUCCESS );
}
