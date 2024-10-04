import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Params, Router, RouterModule } from '@angular/router';
import { LayoutType } from '../../types/layout.type';
import { OrdersComponent } from '../components/orders/orders.component';
import { PromoComponent } from '../components/promo/promo.component';
import { SettingComponent } from '../components/setting/setting.component';
import { HistoryComponent } from '../components/history/history.component';
import { ReviewsComponent } from '../components/reviews/reviews.component';
import { UserComponent } from '../components/user/user.component';

@Component({
  selector: 'lib-profile',
  standalone: true,
  imports: [CommonModule, RouterModule, OrdersComponent, PromoComponent, SettingComponent, HistoryComponent, ReviewsComponent, UserComponent],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss',
})

export class ProfileComponent implements OnInit {
  layouts: LayoutType = {
    user: 'user',
    orders: 'История заказов',
    reviews: 'Мои отзывы',
    promo: 'Промокоды',
    historyOperation: 'История операций',
    setting: 'Настройки',
  }

  currentLayout: string = ''
  link: string = ''

  constructor(private activatedRoute: ActivatedRoute, private router: Router) {
  }

  ngOnInit() {
    this.activatedRoute.queryParams.subscribe((params: Params) => {
      if (params['page']) {
        const page = params['page'];

        if (page && this.layouts[page]) {
          this.currentLayout = this.layouts[page];
          if(this.layouts[page] === this.layouts['user']) {
            this.link = ''
          } else  {
            this.link = this.layouts[page]
          }

        } else {
          this.currentLayout = ''
        }
      } else  {
        this.setUrlParams(this.layouts['user'])

      }
    })
  }

  setUrlParams(page: string): void {
      this.router.navigate([], {
        relativeTo: this.activatedRoute,
        queryParams: { page: page },
        queryParamsHandling: 'merge',
      })

  }

  isLayoutActive(layout: string): boolean {
    return this.currentLayout === this.layouts[layout];
  }

}
