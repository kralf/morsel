#ifndef SPHERICAL_RANGE_CAMERA_H
#define SPHERICAL_RANGE_CAMERA_H

#include "morsel/sensors/range_camera.h"

class SphericalRangeCamera : public RangeCamera
{
public:
  SphericalRangeCamera(
    std::string name,
    double horizontalAngle,
    double verticalAngle,
    double horizontalFOV,
    double verticalFOV,
    int horizontalRays,
    int verticalRays,
    double minRange,
    double maxRange,
    int horizontalResolution = 256,
    int verticalResolution = 256,
    bool acquireColor = false,
    std::string acquireLabel = ""
  );
  virtual ~SphericalRangeCamera();
protected:
  void setupLens();
  void setupRays();
};


#endif /*SPHERICAL_RANGE_CAMERA_H*/
