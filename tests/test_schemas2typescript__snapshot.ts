export enum EnumFruit {
  APPLE = 'APPLE',
  ORANGE = 'ORANGE'
}
export interface NestedSchema {
  string_field: string;
  nullable_datetime_field: string | null;
  recursively_nested_field: NestedSchema | null;
}
export interface ComplexSchema {
  nullable_int_field: number | null;
  nullable_decimal_field: number | null;
  nullable_enum_field: EnumFruit | null;
  nullable_nested_field: NestedSchema | null;
  nested_list_field: Array<NestedSchema>;
}
