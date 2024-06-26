# app/api/routers/anomaly_detector.py
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from application.main.containers import Container
from application.main.domain.entities.product import ProductInput
from application.main.infrastructure.schemas.product import InferenceResponse
from application.main.services.anomaly_detector_service import AnomalyDetectorService

router = APIRouter(prefix="/anomaly-detection")


@router.post("/item_price", response_model=InferenceResponse)
@inject
async def anomaly_price_detector(
    product_info: ProductInput,
    service: AnomalyDetectorService = Depends(
        Provide[Container.anomaly_detector_service]
    ),
):
    try:
        item_id = product_info.item_id
        price = product_info.price

        logger.info(f"detecting anomaly price for item: {item_id} with price: {price}")

        anomaly_response = await service.classify(item_id=item_id, price=price)

        resp = InferenceResponse(
            item_id=item_id, price=price, anomaly=anomaly_response, code=200
        )
        return resp
    except Exception as ex:
        if hasattr(ex, "status_code") and hasattr(ex, "message"):
            logger.error(str(ex))
            raise HTTPException(status_code=ex.status_code, detail=ex.message)
        else:
            logger.error(str(ex))
            raise HTTPException(status_code=500, detail=str(ex))
