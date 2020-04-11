export enum EnumFruit {
  APPLE = 'APPLE',
  ORANGE = 'ORANGE'
}
export interface ComplexSchema {
  nullable_int_field: number | null;
  nullable_decimal_field: number | null;
  nullable_enum_fields: EnumFruit | null;
}
