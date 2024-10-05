import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UserAddressType } from '../../../types/user-address.type';

@Component({
  selector: 'app-user',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user.component.html',
  styleUrl: './user.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class UserComponent implements OnInit {

  public addressArray: UserAddressType = [
    { id: 1, name: 'г. Москва, ул. Солнечная 35', checked: false },
    { id: 2, name: 'г. Москва, ул. Московская 3', checked: false},
    { id: 3, name: 'г. Москва,ул. Октябрьская 1', checked: false},
  ];

  constructor() {}

  ngOnInit() {}

  checkedInput(id: number) {
    this.addressArray.forEach(item => {
      item.checked = (item.id === id)
    })
  }
}
