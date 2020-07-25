from dataclasses import dataclass
from datetime import date
from typing import Optional, NewType


OrderReference = NewType("OrderReference", int)
ProductReference = NewType("ProductReference", str)
OrderQuantity = NewType("OrderQuantity", int)

@dataclass(frozen=True)
class OrderLine: # OrderLine is an immutable dataclass with no behavior.
    orderid: OrderReference
    sku: ProductReference
    qty: OrderQuantity


Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)

class Batch:

    def __init__(
        self, ref: Reference, sku: Sku, qty: Quantity, eta: Optional[date]
        ):
            self.reference = ref
            self.sku = sku
            self.eta = eta
            self._purchased_quantity = qty
            self._allocations = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
