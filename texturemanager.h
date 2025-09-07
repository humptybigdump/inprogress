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

#pragma once
#ifndef TEXTURE_MANAGER
#define TEXTURE_MANAGER

#pragma warning( disable : 4995 )

#include "stdafx.h"
#include <vector>

using namespace std;

#define TEXMAN_SCROLL_DOWN		1
#define TEXMAN_SCROLL_UP		2
#define TEXMAN_NO_MORE_SCROLL	0

class TextureManager
{
	private:
		typedef struct
		{
			char			pSrcFile[1024];
			OGLTexture		*pTexture;
			bool			show;
		}TM_ENTRY;

		vector<TM_ENTRY>	texEntry;
		vector<TM_ENTRY>	texEntryHidden;

#ifdef TEXTURE_MANAGER_GUI
		float				scrollPosition, targetPosition;
		
		int					isVisible, columns, rows, textureManagerScroll;
		int					showR, showG, showB, showA;
		glm::vec4			rgbaExposure;
		float				showAlpha, exposure;
		int					showMip, showFilter;

		int					yOfsLine1, yOfsLine2;

		GLSLProgram			prgRender;			// GLSL programs, each one can keep a vertex and a fragment shader
		bool				shaderLoaded;
		GUIFont				*font;				// a simple bitmap font output
#endif

	public:
		TextureManager();
		~TextureManager();

#ifdef TEXTURE_MANAGER_GUI
		void	reloadShader( bool firstTime = false );
		bool	keyboard( int key, int action );

		void	showTextures();
#endif
		void	addEntry( const char *_pSrcFile, OGLTexture *pTexture, bool _show = true );

		bool	CreateTexture( OGLTexture **ppTexture, int _width, int _height, GLint internalFormat, const char *name = "created by app", bool _show = true  );
		bool	CreateTextureMS( OGLTexture **ppTexture, int _width, int _height, int _nSamples, GLint internalFormat, const char *name = "created by app", bool _show = true  );
		bool	CreateTexture2D( OGLTexture **ppTexture, int _width, int _height, GLint internalFormat, GLint sourceFormat, GLint type, void *ptr, const char *name = "created by app", bool _show = true  );
		bool	CreateTextureFromTGA( OGLTexture **ppTexture, const char *filename, bool _show = true  );
		bool	CreateTextureFromHDR_RGBE( OGLTexture **ppTexture, const char *filename, bool _show = true  );
		bool	CreateTextureFromHDR( OGLTexture **ppTexture, const char *filename, bool _show = true  );
};

#endif


