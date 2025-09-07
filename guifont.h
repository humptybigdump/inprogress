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

#ifndef __GUIFONT__H
#define __GUIFONT__H

class GUIFont
{
	private:
		typedef struct
		{
			int x, y, w, h;
		}CHARACTER;

		int			loaded;
		CHARACTER	charset[ 256 ];

		int			chardata[ 256 * 256 ];

		GLuint		texID;
	protected:
	public:
		GUIFont() : loaded( 0 ) {};

		GUIFont( char *fontname );

		~GUIFont();

		void test();

		int getWidth(const char *str );

		int getHeight(const char *str );

		void print(const char *str, int x, int y );

		void	setMatrices();
};

#endif
