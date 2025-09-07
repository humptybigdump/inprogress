/*
	________             _____      ________________________
	___  __ \______________  /________  ____/__  /___  ____/
	__  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
	_  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
	/_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ simple class to load/access environment maps
*/

#include "stdafx.h"

#ifdef USE_ENVMAP

#pragma warning ( disable : 4996 ) 

using namespace glm;

static float saturate( float x )
{
	if ( x < 0.0f ) return 0.0f;
	if ( x > 1.0f ) return 1.0f;
	return x;
}

vec3 EnvMap::getRandomDirection()
{
	float x = ( rand() / (float)RAND_MAX );
	float y = ( rand() / (float)RAND_MAX );
	float theta = 2.0f * acosf( sqrtf( 1.0f - x ) );
	float phi = 2.0f * static_cast<float>( M_PI ) * y;
	vec3 v( sinf( theta ) * cosf( phi ), sinf( theta ) * sinf( phi ), cosf( theta ) );
	return v;
}

vec2 EnvMap::direction2latlong( vec3 dir )
{
	vec2 uv;

	uv.x = fmodf( atan2f( dir.z, -dir.x ), 2.0f * static_cast<float>( M_PI ) ) / ( 2.0f * static_cast<float>( M_PI ) );
	uv.y = acos( dir.y ) / static_cast<float>( M_PI );
	return uv;
}

void EnvMap::getUV( vec3 dir, int widthEnvMap, int heightEnvMap, int *s, int *t )
{
	vec2 tc = direction2latlong( dir );
	*s = (int)( tc.x * (float)(widthEnvMap)+ (float)widthEnvMap + 0.0f ) % widthEnvMap;
	*t = std::max( 0, (int)std::min( heightEnvMap - 1, (int)( tc.y * (float)heightEnvMap ) ) );
}

vec3 EnvMap::getColor( const vec3 &dir )
{
	int s, t;
	getUV( dir, widthEnvMap, heightEnvMap, &s, &t );

	float r = pEnvMap[ ( s + t * widthEnvMap ) * 4 + 0 ];
	float g = pEnvMap[ ( s + t * widthEnvMap ) * 4 + 1 ];
	float b = pEnvMap[ ( s + t * widthEnvMap ) * 4 + 2 ];
	return vec3( r, g, b );
}

void EnvMap::getUV( const vec3 &dir, int *s, int *t )
{
	getUV( dir, widthEnvMap, heightEnvMap, s, t );
}

vec3 EnvMap::getMaxBrightness()
{
	vec3 maxBrightness = vec3( 0.0f );
	for ( int s = 0; s < widthEnvMap; s++ )
		for ( int t = 0; t < heightEnvMap; t++ )
		{
			float r = pEnvMap[ ( s + t * widthEnvMap ) * 4 + 0 ];
			float g = pEnvMap[ ( s + t * widthEnvMap ) * 4 + 1 ];
			float b = pEnvMap[ ( s + t * widthEnvMap ) * 4 + 2 ];
			vec3 c = vec3( r, g, b );
			maxBrightness.x = glm::max( maxBrightness.x, r );
			maxBrightness.y = glm::max( maxBrightness.y, g );
			maxBrightness.z = glm::max( maxBrightness.z, b );
		}
	return maxBrightness;
}

#endif