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

#pragma once
#ifndef __LENS_H
#define __LENS_H

#pragma warning( disable : 4995 )

using namespace std;

class ScreenLens
{
	private:
		GLSLProgram			prgRender;
		bool				shaderLoaded;
		GUIFont				*font;

		int					isVisible, zoom;
		int					updatePosition;

		int					quadrant;
		float				targetX, targetY, posX, posY;
		int					Width, Height, first;
		double				dx, dy;

	public:
		ScreenLens();
		~ScreenLens();
		
		void	reloadShader( bool firstTime = false );

		void	showLens( GLuint texture, bool multisample = false, float scale = 1.0f );
		bool	keyboard( int key, int action );
};

#endif


