/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ simple OpenGL texture loading/handling
*/

#ifndef __TEXTURE_H
#define __TEXTURE_H

class OGLTexture
{
private:
	GLenum	target;
	GLuint	ID;

	int		width, height;
	int		numSamples;
	int		format;

	void	deleteTexture();

public:
	OGLTexture( GLenum _target = GL_TEXTURE_2D );
	~OGLTexture();

	bool	createTexture();

	// get some info
	GLuint	getID()       { return ID-1; };
	int		getWidth()    { return width; };
	int		getHeight()   { return height; };
	int		getFormat()   { return format; };
	GLenum  getTarget()	  { return target; };
	int		getNSamples() { return numSamples; };

	// create textures without and with multisampling
	bool	createTexture2D( int _width, int _height, GLint internalFormat );
	bool	createTexture2DMS( int _width, int _height, int _numSamples, GLint internalFormat );

	// load textures
	bool	loadHDR_RGBE  ( const char *filename ); // .hdr as RGB + Exponent (4x 8 Bit)
	bool	loadHDR_FLOAT ( const char *filename ); // .hdr as FP texture
	bool	loadTGA		  ( const char *fileName ); // .tga (24 or 32 bit)

	void	bind();
	void	bind( GLint unit );
};

#endif
