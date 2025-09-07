/*
    ________             _____      ________________________
    ___  __ \______________  /________  ____/__  /___  ____/
    __  /_/ /_  ___/  __ \  __/  __ \  / __ __  / __  /_
    _  ____/_  /   / /_/ / /_ / /_/ / /_/ / _  /___  __/
    /_/     /_/    \____/\__/ \____/\____/  /_____/_/

   ___/ minimalistic prototyping framework for OpenGL demos and practical courses
   ___/ Carsten Dachsbacher
   ___/ (ASCII font generator: http://patorjk.com/software/taag/)

   ___/ simple binary file IO routines
*/

#ifndef _FILE_IO_H
#define _FILE_IO_H

#include <iostream>
#include <fstream>

class _FILEIO {
private:
    FILE* f;
#ifdef FILE_IO_USE_STREAMS
	ofstream *_of;
	ifstream *_if;
public:
	_FILEIO() : _of( NULL ), _if(NULL) {};
#else

public:
    _FILEIO() {
    };
#endif

    ~_FILEIO() {
    };

#ifndef FILE_IO_USE_STREAMS
    bool readFile(char* name) {
        f = fopen(name, "rb");
        if (f == NULL) return false;
        return true;
    };

    bool writeFile(char* name) {
        f = fopen(name, "wb");
        if (f == NULL) return false;
        return true;
    };

    bool closeFile() {
        if (f != NULL) fclose(f);
        return true;
    };
    bool eof() { return feof(f) > 0; };
    void seek(int ofs, int from) { fseek(f, ofs, from); };
    int tell() { return ftell(f); };
    int error() { return ferror(f); };
    int get(void* buf, int size) { return (int) fread(buf, 1, size, f); };
    int put(const void* buf, int size) { return (int) fwrite(buf, 1, size, f); };

#else
	bool		readFile( char *name ) { _if = new ifstream( "tt", ios::in | ios::ate | ios::binary ); if ( !_if->is_open() ) return false; return true; };
	bool		writeFile( char *name ) { _of = new ofstream( "tt", ios::out | ios::app | ios::binary ); if ( !_of->is_open() ) return false; return true; };
	bool		closeFile()
	{
		if ( _of->is_open() ) { _of->close(); _of = NULL; return true; }
		if ( _if->is_open() ) { _if->close(); _if = NULL; return true; }
		return false;
	};

	int			tell() { if ( _of->is_open() ) return _of->tellp(); return -1; };
	int			get( void *buf, int size ) { _if->read( (char*)buf, size ); return size; /*HACK*/ };
	int			put( const void *buf, int size ) { _of->write( (char*)buf, size ); return size; /*HACK*/ };
#endif

    unsigned char getU8() {
        unsigned char x;
        get(&x, 1);
        return x;
    };

    unsigned short getU16() {
        unsigned short x;
        get(&x, sizeof(unsigned short));
        return x;
    };

    unsigned int getU32() {
        unsigned int x;
        get(&x, sizeof(unsigned int));
        return x;
    };

    signed char getS8() {
        signed char x;
        get(&x, 1);
        return x;
    };

    signed short getS16() {
        signed short x;
        get(&x, sizeof(signed short));
        return x;
    };

    signed int getS32() {
        signed int x;
        get(&x, sizeof(signed int));
        return x;
    };

    float getF32() {
        float x;
        get(&x, sizeof(float));
        return x;
    };

    double getD32() {
        double x;
        get(&x, sizeof(double));
        return x;
    };

    glm::vec3 getV32() {
        glm::vec3 x;
        get(&x.x, sizeof(float));
        get(&x.y, sizeof(float));
        get(&x.z, sizeof(float));
        return x;
    };

    glm::vec4 getF4() {
        glm::vec4 x;
        get(&x.x, sizeof(float));
        get(&x.y, sizeof(float));
        get(&x.z, sizeof(float));
        get(&x.w, sizeof(float));
        return x;
    };

    void getF3(float* d) {
        get(&d[0], sizeof(float));
        get(&d[1], sizeof(float));
        get(&d[2], sizeof(float));
    };

    bool putU8(unsigned char x) { return put(&x, 1) == 1; };
    bool putU16(unsigned short x) { return put(&x, 2) == 2; };
    bool putU32(unsigned int x) { return put(&x, 4) == 4; };
    bool putS8(signed char x) { return put(&x, 1) == 1; };
    bool putS16(signed short x) { return put(&x, 2) == 2; };
    bool putS32(signed int x) { return put(&x, 4) == 4; };
    bool putF32(float x) { return put(&x, 4) == 4; };

    bool putV32(glm::vec3& x) {
        return put(&x.x, sizeof(float)) == sizeof(float) && put(&x.y, sizeof(float)) == sizeof(float) &&
               put(&x.z, sizeof(float)) == sizeof(float);
    };

    bool putF4(glm::vec4& x) {
        return put(&x.x, sizeof(float)) == sizeof(float) && put(&x.y, sizeof(float)) == sizeof(float) &&
               put(&x.z, sizeof(float)) == sizeof(float) && put(&x.w, sizeof(float)) == sizeof(float);
    };

    bool putF3(float* x) {
        return put(&x[0], sizeof(float)) == sizeof(float) && put(&x[1], sizeof(float)) == sizeof(float) &&
               put(&x[2], sizeof(float)) == sizeof(float);
    };

    bool getString(char* s, int size) {
        int l = 0;

        for (;;) {
            if (get(s, 1) != 1)
                return false;

            if (!*s++) break;

            if (++l >= size)
                return false;
        }

        return !ferror(f);
    }

    bool putString(const char* s) {
        put(s, (int) strlen(s) + 1);
        return (bool) !ferror(f);
    }

    bool getString(unsigned short* s, int size) {
        int l = 0;

        for (;;) {
            if (get(s, sizeof(unsigned short)) != sizeof(unsigned short))
                return false;

            if (!*s++) break;

            if (++l >= size)
                return false;
        }

        return !ferror(f);
    }

    bool putString(const wchar_t* s) {
        put(s, (int) wcslen(s) * 2 + 2);
        return (bool) !ferror(f);
    }
};


#endif
