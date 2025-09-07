#include <cglib/core/glheaders.h>
#include <cglib/core/assert.h>

#include <cglib/gl/device_rendering_context.h>
#include <cglib/gl/device_render.h>
#include <cglib/gl/renderer.h>

#include "renderers.h"

int
main(int argc, char const**argv)
{
	DeviceRenderingContext context;
    if (!context.params.parse_command_line(argc, argv)) {
        std::cerr << "invalid command line argument" << std::endl;
        return -1;
    }

	context.renderers.push_back(std::make_shared<ShadowVolumes>());

    return DeviceRender::run(context, GUI::DEFAULT_FLAGS);
}
// CG_REVISION 5ad5f3ea62d3114bee96949072042ec297d654c5
