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

#include "stdafx.h"

#pragma warning ( disable : 4996 ) 

OGLTexture::OGLTexture( GLenum _target )
{
	ID = 0;
	target = _target;
}

OGLTexture::~OGLTexture()
{
	deleteTexture();
}

bool OGLTexture::createTexture()
{
	deleteTexture();

	glGenTextures( 1, &ID );

	ID ++;

	glBindTexture  ( target, ID - 1 );
	glTexParameterf( target, GL_TEXTURE_WRAP_S, GL_REPEAT );
	glTexParameterf( target, GL_TEXTURE_WRAP_T, GL_REPEAT );
	glTexParameterf( target, GL_TEXTURE_MAG_FILTER, GL_LINEAR );
	glTexParameterf( target, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR );

	width = height = 0;
	numSamples = 0;
	format = -1;

	return true;
}

void OGLTexture::deleteTexture()
{
	if ( ID )
	{
		ID --;
		glDeleteTextures( 1, &ID );
		ID = 0;
	}
}

void OGLTexture::bind()
{
	glBindTexture( target, ID - 1 );
}

void OGLTexture::bind( GLint unit )
{
	glBindMultiTextureEXT( unit, target, ID - 1 );
}

bool OGLTexture::createTexture2D( int _width, int _height, GLint internalFormat ) {
	deleteTexture();
	glGenTextures( 1, &ID );
	ID ++;
	width = _width; height = _height;
	format = internalFormat;
	numSamples = 0;

	glBindTexture  ( GL_TEXTURE_2D, ID - 1 );
	glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST );
	glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST );

	glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP );
	glTexParameteri ( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP );
	glTexImage2D ( GL_TEXTURE_2D, 0, internalFormat, width, height, 0, GL_RGB, GL_FLOAT, 0 );
	return true;
}

bool OGLTexture::createTexture2DMS( int _width, int _height, int _numSamples, GLint internalFormat ) {
	deleteTexture();
	glGenTextures( 1, &ID );
	ID ++;
	width = _width; height = _height;
	format = internalFormat;
	target = GL_TEXTURE_2D_MULTISAMPLE;
	numSamples = _numSamples;

	glBindTexture  ( GL_TEXTURE_2D_MULTISAMPLE, ID - 1 );
	glTexImage2DMultisample( GL_TEXTURE_2D_MULTISAMPLE, numSamples, internalFormat, width, height, true );
	return true;
}

bool OGLTexture::loadHDR_RGBE( const char *filename )
{
	createTexture();

	FILE *f = fopen( filename, "rb" );
	
	if ( !f ) 
	{
		fprintf( stderr, " [TEX]: could not open file '%s'\n", filename );
		return false;
	}

	rgbe_header_info header;
	if ( RGBE_ReadHeader( f, &width, &height, &header ) )
	{
		fprintf( stderr, " [TEX]: problem with header of '%s'\n", filename );
		return false;
	}

	//  img.data = new float[m_width*m_height*3];
	unsigned char *data = new unsigned char[ width * height * 4 ];
	if ( !data )
		return false;

	//  if (RGBE_ReadPixels_RLE(fp, img.data, img.width, img.height))
	if ( RGBE_ReadPixels_Raw_RLE( f, data, width, height ) )
	{
		fprintf( stderr, " [TEX]: problem with image data of '%s'\n", filename );
		return false;
	}

	fclose( f );

	fprintf( stderr, " [TEX]: loaded '%s'\n", filename );

	glTexImage2D( target, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data );
	glGenerateMipmap( GL_TEXTURE_2D );

	format = GL_RGBA;

	delete [] data;

	return true;
}

bool OGLTexture::loadHDR_FLOAT( const char *filename )
{
	createTexture();

	FILE *f = fopen( filename, "rb" );
	
	if ( !f ) 
	{
		fprintf( stderr, " [TEX]: could not open file '%s'\n", filename );
		return false;
	}

	rgbe_header_info header;
	if ( RGBE_ReadHeader( f, &width, &height, &header ) )
	{
		fprintf( stderr, " [TEX]: problem with header of '%s'\n", filename );
		return false;
	}

	//  img.data = new float[m_width*m_height*3];
	unsigned char *data = new unsigned char[ width * height * 4 ];
	if ( !data )
		return false;

	//  if (RGBE_ReadPixels_RLE(fp, img.data, img.width, img.height))
	if ( RGBE_ReadPixels_Raw_RLE( f, data, width, height ) )
	{
		fprintf( stderr, " [TEX]: problem with image data of '%s'\n", filename );
		return false;
	}

	fclose( f );

	float *fdata = new float[ width * height * 4 ];
	float *dst = fdata;
	unsigned char *src = data;
	for ( int i = 0; i < width * height; i++, dst += 4, src += 4 )
	{
		rgbe2float( &dst[ 0 ], &dst[ 1 ], &dst[ 2 ], src );
		
		// when accessed as a RGBE texture, this is the correct exponent
		dst[ 3 ] = 128.0f / 255.0f;
	}

	fprintf( stderr, " [TEX]: loaded '%s'\n", filename );

	glTexImage2D( target, 0, GL_RGBA32F_ARB, width, height, 0, GL_RGBA, GL_FLOAT, fdata );
	glGenerateMipmap( GL_TEXTURE_2D );

	format = GL_RGBA32F_ARB;
	
	delete [] data;
	delete [] fdata;

	return true;
}

#define TGA_RGB		 2		// RGB file
#define TGA_A		 3		// ALPHA file
#define TGA_RLE		10		// run-length encoded

bool OGLTexture::loadTGA( const char *filename )
{
	unsigned short wwidth, 
				   wheight;
	unsigned char  length, 
				   imageType, 
				   bits;
	unsigned long  stride, 
				   channels;
	unsigned char *data;

	width = height = 0;
	createTexture();
	
	FILE *f;

	if( ( f = fopen( filename, "rb" ) ) == NULL ) 
	{
		fprintf( stderr, " [TEX]: could not open file '%s'\n", filename );
		return false;
	}
		
	fread( &length, sizeof( unsigned char ), 1, f );
	fseek( f, 1, SEEK_CUR );
	fread( &imageType, sizeof( unsigned char ), 1, f );
	fseek( f, 9, SEEK_CUR ); 

	fread( &wwidth,  sizeof( unsigned short ), 1, f );
	fread( &wheight, sizeof( unsigned short ), 1, f );
	fread( &bits,    sizeof( unsigned char ), 1, f );
	
	width  = wwidth;
	height = wheight;

	fseek( f, length + 1, SEEK_CUR ); 

	// umcompressed image file
	if( imageType != TGA_RLE )
	{
		// true color
		if( bits == 24 || bits == 32 )
		{
			channels = bits / 8;
			stride   = channels * width;
			data     = new unsigned char[ stride * height ];

			for( int y = 0; y < height; y++ )
			{
				unsigned char *pLine = &( data[ stride * y ] );

				fread( pLine, stride, 1, f );
			
				for( int i = 0; i < (int)stride; i += channels )
				{
					int temp	   = pLine[ i ];
					pLine[ i ]     = pLine[ i + 2 ];
					pLine[ i + 2 ] = temp;
				}
			}
		} else 
		// hi color
		if( bits == 16 )
		{
			unsigned short pixels = 0;
			int r, g, b;

			channels = 3;
			stride   = channels * width;
			data     = new unsigned char[ stride * height ];

			for( int i = 0; i < (int)(width*height); i++ )
			{
				fread( &pixels, sizeof(unsigned short), 1, f );
				
				b =   ( pixels & 0x1f ) << 3;
				g = ( ( pixels >> 5 ) & 0x1f ) << 3;
				r = ( ( pixels >> 10 ) & 0x1f ) << 3;
				
				data[ i * 3 + 0 ] = r;
				data[ i * 3 + 1 ] = g;
				data[ i * 3 + 2 ] = b;
			}
		} else
			return false;
	} else
	// RLE compressed image
	{
		unsigned char rleID = 0;
		int colorsRead = 0;
		
		channels = bits / 8;
		stride   = channels * width;

		data = new unsigned char[ stride * height ];
		unsigned char *pColors = new unsigned char [ channels ];

		int i = 0;
		while( i < width * height )
		{
			fread( &rleID, sizeof( unsigned char ), 1, f );
			
			if( rleID < 128 )
			{
				rleID++;

				while( rleID )
				{
					fread( pColors, sizeof( unsigned char ) * channels, 1, f );

					data[ colorsRead + 0 ] = pColors[ 2 ];
					data[ colorsRead + 1 ] = pColors[ 1 ];
					data[ colorsRead + 2 ] = pColors[ 0 ];

					if ( bits == 32 )
						data[ colorsRead + 3 ] = pColors[ 3 ];

					i ++;
					rleID --;
					colorsRead += channels;
				}
			} else
			{
				rleID -= 127;

				fread( pColors, sizeof( unsigned char ) * channels, 1, f );

				while( rleID )
				{
					data[ colorsRead + 0 ] = pColors[ 2 ];
					data[ colorsRead + 1 ] = pColors[ 1 ];
					data[ colorsRead + 2 ] = pColors[ 0 ];

					if ( bits == 32 )
						data[ colorsRead + 3 ] = pColors[ 3 ];

					i ++;
					rleID --;
					colorsRead += channels;
				}
			}
		}

		delete [] pColors;
	}

	fclose( f );

	if ( channels == 4 ) {
		format = GL_RGBA;
		glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data );
		glGenerateMipmap( GL_TEXTURE_2D );
	} else {
		format = GL_RGB;
		glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data );
		glGenerateMipmap( GL_TEXTURE_2D );
	}

	delete [] data;

	fprintf( stderr, " [TEX]: loaded '%s'\n", filename );

	return true;
}

