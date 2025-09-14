function patch = extract_image_patch(I, p, patch_dim)
%EXTRACT_IMAGE_PATCH Extracts a block from an image and
% returns this block as an NxM matrix. I is the image, p is the center
% point of the patch, while patch_dim as [height, width] specifies the dimensions
% of the patch around the center. 
    u = p(1);
    v = p(2);
    [height, width] = size(I);
    patch_height = patch_dim(1);
    patch_width = patch_dim(2);
    if (width == 0 || height == 0) 
        error('Invalid dimension specified')
    end
    if (u < 1 || u > width)
        error('Invalid u-coordinate specified');
    end
    if (v < 1 || v > height)
        error('Invalid v-coordinate specified');
    end
    if ((mod(patch_width,2) == 0) || (mod(patch_height,2) == 0))
        error('The patch dimensions must be odd.');
    end
    patch_half_len_u = (patch_width-1) / 2;
    patch_half_len_v = (patch_height-1) / 2;
    if ((u - patch_half_len_u >= 1) && (u + patch_half_len_u <= width) && ...
        (v - patch_half_len_v >= 1) && (v + patch_half_len_v <= height))
        patch = I(v - patch_half_len_v:v + patch_half_len_v,u-patch_half_len_u:u+patch_half_len_u);
    else
        % handle the corner cases at the boundaries
        patch = zeros(patch_height, patch_width, 'uint8');
        for pv = -patch_half_len_v:1:patch_half_len_v
            for pu = -patch_half_len_u:1:patch_half_len_u
                iv = v + pv;
                iu = u + pu;
                % clipping in border areas
                if (iv >= 1 && iv <= height && iu >= 1 && iu <= width)
                    val = I(iv, iu);
                else if (iv >= 1 && iv <= height && (iu < 1 || iu > width))
                        val = I(iv, 1)*uint8(iu < 1) + I(iv, width)*uint8(iu > width);
                    else if ((iv < 1 || iv > height) && iu >= 1 && iu <= width)
                            val = I(1, iu)*uint8(iv < 1) + I(height, iu)*uint8(iv > height);
                        else
                            val = I(1,1)*uint8(iv < 1 && iu < 1) + I(1,width)*uint8(iv < 1 && iu > width) + ...
                                    I(height,width)*uint8(iv > height && iu > width) + I(height,1)*uint8(iv > height && iu < 1);
                        end
                    end
                end
                patch(pv + patch_half_len_v + 1, pu + patch_half_len_u + 1) = val;
            end
        end
    end
end

