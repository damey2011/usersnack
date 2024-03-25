from typing import Any, Dict, List
from uuid import UUID


def build_order_in(pizza_id: UUID, extras: List[UUID], **kwargs) -> Dict[str, Any]:
    return {
        "name": "Damilola Adeyemi",
        "contact_phones": ["08132998226"],
        "delivery_address": {
            "street": "Femi Soluade",
            "house_number": "18A",
            "apt": "2",
            "city": "Lagos",
            "country": "Nigeria",
        },
        "packages": [
            {
                "pizza_id": str(pizza_id),
                "garnishes": [
                    {
                        "extra_id": str(extra_id),
                        "quantity": kwargs.get("extra_quantity", 1),
                    }
                    for extra_id in extras
                ],
                "quantity": kwargs.get("pizza_quantity", 1),
            }
        ],
    }
